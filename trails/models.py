from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator


class Trail(models.Model):

    TYPE_CHOICES = [
        ('swim', 'Swim'),
        ('bike', 'Bike'),
        ('run', 'Run'),
    ]

    name = models.CharField(max_length=100)
    trail_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    country = models.CharField(max_length=20)
    city_town = models.CharField(max_length=20)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Latitude between -90 and 90 degrees"
        )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Longitude between -180 and 180 degrees"
        )
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    elevation_gain = models.IntegerField()
    description = models.TextField()
    images = ArrayField(
        models.URLField(),
        size=8,
    )

    created_by = models.ForeignKey(
        to='users.User',
        related_name='trails_owned',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name}'
