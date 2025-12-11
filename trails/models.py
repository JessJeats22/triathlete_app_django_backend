from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
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
    location = models.PointField()
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    elevation_gain = models.IntegerField()
    description = models.TextField()
    images = ArrayField(
        models.ImageField(upload_to='trails/images/',
        size=8,
        blank=True,
        nul=True,
        default=list
        )
    )
    created_by = models.ForeignKey(
        to='users.User', 
        related_name='trails_owned', 
        on_delete=models.CASCADE 
    )
 


    def __str__(self):
        return f'{self.name}'