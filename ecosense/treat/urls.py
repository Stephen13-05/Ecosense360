from django.urls import path
from .views import get_tailored_recommendations
from .views import download_pdf

app_name = "treat"

urlpatterns = [
    path("recommendations/", get_tailored_recommendations, name="get_recommendations"),
    path('download/', download_pdf, name='download_pdf'),

]
