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

