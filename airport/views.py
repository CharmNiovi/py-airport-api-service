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
from core.permissions import IsAdminOrReadOnly, OrderSpecialPermission


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
