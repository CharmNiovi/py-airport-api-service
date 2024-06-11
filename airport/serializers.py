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

