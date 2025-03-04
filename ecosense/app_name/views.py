from django.shortcuts import render, redirect
from django.contrib.auth import login 
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from googletrans import Translator
from django.utils.translation import activate
from django.http import HttpResponse

@login_required
def home_view(request):
    return render(request,"registration/home.html")

def carbon_calculator_view(request):
    return render(request,"registration/carbon_calc.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        form = UserCreationForm({
            "username": username,
            "password1": password1,
            "password2": password2,
        })

        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect("login")  # Ensure a valid redirect after successful signup
    else:
        form = UserCreationForm()  # Handle GET request properly
       
    
    return render(request, "registration/signup.html", {"form": form})  # Always return a response

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")  # Redirect to home page after login

    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})

def home(request):
    translator = Translator()
    
    user_language = request.GET.get('lang', 'en')  # Get language from query parameter
    text = "Welcome to our website"  
    
    translated_text = translator.translate(text, dest=user_language).text
    
    return render(request, "home.html", {"message": translated_text})    

def set_language(request):
    if request.method == "POST":
        lang = request.POST.get('language', 'en')
        activate(lang)
        request.session['django_language'] = lang
        return redirect(request.META.get('HTTP_REFERER', '/'))    

    