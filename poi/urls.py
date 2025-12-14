from django.urls import path
from .views import POIListCreateView, POIDetailView

urlpatterns = [
    path('trails/<int:trail_id>/pois/',POIListCreateView.as_view()),
    path('<int:pk>/', POIDetailView.as_view())
]