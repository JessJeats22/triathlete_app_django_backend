from django.urls import path
from trails.views import TrailShowView, TrailDetailView



# Every request that hits this router file, will already start with `/trails/`
urlpatterns = [
    path('', TrailShowView.as_view()),
    path('<int:pk>/', TrailDetailView.as_view()),
]