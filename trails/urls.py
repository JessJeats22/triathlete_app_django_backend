from django.urls import path
from trails.views import TrailShowView, TrailDetailView, TrailFavouriteView



# Every request that hits this router file, will already start with `/trails/`
urlpatterns = [
    path('', TrailShowView.as_view()),
    path('<int:pk>/', TrailDetailView.as_view()),
    path('<int:pk>/favourite/', TrailFavouriteView.as_view()),
]