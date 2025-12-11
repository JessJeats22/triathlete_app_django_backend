from django.db import models

# Create your models here.
class PointOfInterest(models.Model):

    name = models.CharField(max_length=100)
    category_type =  models.CharField(max_length=20)
    description = models.TextField(max_length=1000)
    location = models.PointField()
    owner = models.ForeignKey(
        to='users.User',
        related_name='points_of_interest',
        on_delete=models.CASCADE
    )


    def __str__(self):
        return self.name