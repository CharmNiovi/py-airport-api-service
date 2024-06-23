from django.urls import include, path
from rest_framework.routers import DefaultRouter
from airport.views import (
    CountryViewSet,
    CityViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    AirportViewSet,
    RouteViewSet,
    CrewViewSet,
    FlightViewSet,
    TicketViewSet,
    OrderViewSet,
)
router = DefaultRouter()
router.register("country", CountryViewSet, basename="country")
router.register("city", CityViewSet, basename="city")
router.register("airplane-type", AirplaneTypeViewSet, basename="airplane-type")
router.register("airplane", AirplaneViewSet, basename="airplane")
router.register("airport", AirportViewSet, basename="airport")
router.register("route", RouteViewSet, basename="route")
router.register("crew", CrewViewSet, basename="crew")
router.register("flight", FlightViewSet, basename="flight")
router.register("order", OrderViewSet, basename="order")
router.register("ticket", TicketViewSet, basename="ticket")

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
