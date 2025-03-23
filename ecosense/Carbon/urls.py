from django.urls import path
from .views import carbon_footprint

urlpatterns = [
    path("carbon/", carbon_footprint, name="carbon_footprint"),
]
