from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


class AirplaneType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField(validators=[MinValueValidator(1)])
    seats_per_row = models.IntegerField(validators=[MinValueValidator(1)])
    airplane_type = models.ForeignKey(AirplaneType,
                                      on_delete=models.CASCADE,
                                      related_name="airplanes")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "airplane_type"],
                name="unique_airplane"
            ),
        ]

    def __str__(self):
        return self.name

    @property
    def capacity(self):
        return self.rows * self.seats_per_row


class Country(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=250, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")

    def __str__(self) -> str | models.CharField:
        return self.name

    class Meta:
        ordering = ("name",)


class Airport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    closest_big_city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, related_name="airports"
    )

    def __str__(self):
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="sources")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="destinations")
    distance = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.source} - {self.destination} ({self.distance})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "destination"],
                name="unique_route"
            ),
        ]


class Flight(models.Model):
    crew = models.ManyToManyField(Crew, related_name="flights")
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

