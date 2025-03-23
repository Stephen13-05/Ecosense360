from django.urls import path
from .views import carbon_footprint
from .views import carbon_result

urlpatterns = [
    path("carbon/", carbon_footprint, name="carbon_footprint"),
    path("carbon/result/", carbon_result, name="carbon_result"),
]
