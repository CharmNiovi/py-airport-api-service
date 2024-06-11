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

