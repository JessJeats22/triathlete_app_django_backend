from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class PointOfInterest(models.Model):

    name = models.CharField(max_length=100)
   
    description = models.TextField(max_length=1000)

    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Latitude between -90 and 90 degrees"
        )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Longitude between -180 and 180 degrees"
        )

    created_by = models.ForeignKey(
        to='users.User',
        related_name='points_of_interest',
        on_delete=models.CASCADE
    )

    trail = models.ForeignKey(
        to='trails.Trail',
        related_name='points_of_interest',
        on_delete=models.CASCADE,
        null=True,
        blank=True
)

    def __str__(self):
        return self.name
