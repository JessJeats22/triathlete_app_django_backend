from django.urls import path
from .views import SignUpView


# All requests hitting this router already start with `auth/`
urlpatterns = [
    path('sign-up/', SignUpView.as_view())
    ]