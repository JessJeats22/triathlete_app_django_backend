from django.urls import path
from .views import POIListCreateView

urlpatterns = [
    path('trails/<int:trail_id>/pois/',POIListCreateView.as_view())
]