from django.db import models

# Create your models here.
class PointOfInterest(models.Model):

    TYPE_CHOICES = [
        ('pub', 'Pub'),
        ('water_point', 'Water Point'),
        ('café', 'Café'),
        ('viewpoint', 'Viewpoint'),
        ('bike_shop', 'Bike Shop'),
        ('other', 'Other'),
        ]
    
    name = models.CharField(max_length=100)
    category_type =  models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(max_length=1000)