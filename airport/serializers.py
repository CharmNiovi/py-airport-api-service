from rest_framework import serializers

from .models import (
    City,
    Country,
    AirplaneType,
    Airplane,
    Route,
    Crew,
    Airport,
    Flight,
    Ticket,
    Order,
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = "__all__"


class CityWithSlugSerializer(CitySerializer):
    country = serializers.SlugRelatedField(slug_field="name", read_only=True)


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = "__all__"


class AirplaneRetrieveSerializer(AirplaneSerializer):
    airplane_type = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True
    )
    airplane_type_url = serializers.HyperlinkedIdentityField(
        view_name="airport:airplane-type-detail",
        lookup_field="pk"
    )


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True
    )
    airplane_type_url = serializers.HyperlinkedIdentityField(
        view_name="airport:airplane-type-detail",
        lookup_field="get_airplane_type_pk",
        lookup_url_kwarg="pk",
        read_only=True
    )

    class Meta:
        model = Airplane
        fields = ("id", "name", "capacity", "airplane_type", "airplane_type_url")


class AirplaneNestedSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="airport:airplane-detail",
        lookup_field="pk",
        read_only=True
    )

    class Meta:
        model = Airplane
        fields = ("id", "name", "capacity", "url")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"


class AirplaneTypeDetailSerializer(AirplaneTypeSerializer):
    airplanes = AirplaneNestedSerializer(many=True, read_only=True)


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"


class RouteWithSlugSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(slug_field="name", read_only=True)
    destination = serializers.SlugRelatedField(slug_field="name", read_only=True)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class AirportListSerializer(AirportSerializer):
    closest_big_city = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True
    )


class AirportDetailSerializer(serializers.ModelSerializer):
    sources = RouteWithSlugSerializer(
        many=True,
        read_only=True
    )
    destinations = RouteWithSlugSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Airport
        fields = "__all__"


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class RouteNestedSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="airport:route-detail",
        lookup_field="pk",
        read_only=True
    )
    source = serializers.SlugRelatedField(slug_field="name", read_only=True)
    destination = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Route
        fields = ("source", "destination", "url")


class FlightNestedSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="airport:flight-detail",
        lookup_field="pk",
        read_only=True
    )
    route = RouteNestedSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = ("url", "route")


class CrewDetailSerializer(CrewSerializer):
    flights = FlightNestedSerializer(many=True, read_only=True)


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = "__all__"


class CrewNestedSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="airport:crew-detail",
        lookup_field="pk",
        read_only=True
    )

    class Meta:
        model = Crew
        fields = ("url", "first_name", "last_name")


class FlightDetailSerializer(FlightSerializer):
    #TODO: вільні ticketи
    crew = CrewNestedSerializer(many=True, read_only=True)
    route = RouteNestedSerializer(read_only=True)
    airplane = AirplaneNestedSerializer(read_only=True)


class FlightListSerializer(FlightSerializer):
    route = RouteNestedSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = ("departure_time", "arrival_time", "route")

