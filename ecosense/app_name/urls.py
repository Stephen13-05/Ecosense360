from django.urls import path, include
from django.contrib.auth.views import LoginView  
from .views import signup_view
from .views import login_view
from .views import home_view
from .views import carbon_calculator_view
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.i18n import set_language


urlpatterns = [
    path("home/", home_view, name="home"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("carbon_calculator/", carbon_calculator_view, name="carbon_calculator"),
    path("accounts/", include("django.contrib.auth.urls")),
   path("set-language/", set_language, name="set_language"),
]  

urlpatterns += [path("i18n/", include("django.conf.urls.i18n"))]  # Keep this 