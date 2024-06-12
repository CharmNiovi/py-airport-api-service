from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from airport.models import (
    City,
    Country,
    AirplaneType,
    Airplane,
    Route,
    Crew,
    Airport,
    Order,
    Flight,
    Ticket,
)
from airport.serializers import (
    CitySerializer,
    CityWithSlugSerializer,
    CountrySerializer,
    AirplaneTypeSerializer,
    AirplaneTypeDetailSerializer,
    AirplaneListSerializer,
    AirplaneSerializer,
    AirplaneRetrieveSerializer,
    AirportSerializer,
    AirportListSerializer,
    AirportDetailSerializer,
    RouteSerializer,
    RouteWithSlugSerializer,
    CrewSerializer,
    CrewDetailSerializer,
    OrderAdminSerializer,
    OrderUserSerializer,
    OrderDetailSerializer,
    FlightSerializer,
    FlightDetailSerializer,
    FlightListSerializer,
    TicketSerializer,
    TicketDetailSerializer,
    TicketUnableToBuySerializer,
)
from core.permissions import IsAdminOrReadOnly, UserCantUpdateAndDeletePermission


class CountryViewSet(ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)


class CityViewSet(ModelViewSet):
    queryset = City.objects.select_related("country")
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return CityWithSlugSerializer
        return CitySerializer


class AirplaneTypeViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AirplaneTypeDetailSerializer
        return AirplaneTypeSerializer

    def get_queryset(self):
        queryset = AirplaneType.objects.all()
        if self.action == "retrieve":
            return queryset.prefetch_related("airplanes")
        return queryset


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneRetrieveSerializer
        return AirplaneSerializer


class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.select_related("closest_big_city")
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action == "list":
            return AirportListSerializer
        if self.action == "retrieve":
            return AirportDetailSerializer
        return AirportSerializer


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return RouteWithSlugSerializer
        return RouteSerializer


class CrewViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CrewDetailSerializer
        return CrewSerializer

    def get_queryset(self):
        queryset = Crew.objects.all()
        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                "flights__route__source",
                "flights__route__destination",
            )
        return queryset


class FlightViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer

    def get_queryset(self):
        queryset = Flight.objects.all()
        if self.action == "list":
            queryset = queryset.select_related()
        if self.action == "retrieve":
            queryset = queryset.prefetch_related("crew")
            queryset = queryset.select_related()
        return queryset

    @action(detail=True, methods=["get"])
    def tickets(self, request, pk):
        tickets = self.get_object().tickets.all()
        serializer = TicketUnableToBuySerializer(tickets, many=True)
        return Response(serializer.data)


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated, UserCantUpdateAndDeletePermission)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        queryset = Ticket.objects.select_related()
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return queryset
        return queryset.filter(order__user=user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TicketDetailSerializer
        return TicketSerializer


class OrderViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin
):
    permission_classes = (IsAuthenticated, UserCantUpdateAndDeletePermission,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        queryset = Order.objects.all()
        user = self.request.user

        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                "tickets__flight__route__source",
                "tickets__flight__route__destination",
            )
        if user.is_staff or user.is_superuser:
            return queryset
        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return OrderAdminSerializer
        return OrderUserSerializer
