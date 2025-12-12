from django.urls import path
from trails.views import TrailShowView



# Every request that hits this router file, will already start with `/trails/`
urlpatterns = [
    path('', TrailShowView.as_view()),
]