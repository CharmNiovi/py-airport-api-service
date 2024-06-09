from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


class AirplaneType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

