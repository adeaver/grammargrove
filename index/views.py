from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.template import loader

@ensure_csrf_cookie
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', {})

def login(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect("/?error=bad_req")
    user = authenticate(username=request.POST["email"], password=request.POST["password"])
    if not user:
        return redirect("/?error=bad_auth")
    else:
        login(request, user)
        return redirect("/dashboard/")

@login_required(login_url="/")
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, 'dashboard.html', {})

@login_required(login_url="/")
def quiz(request: HttpRequest) -> HttpResponse:
    return render(request, 'quiz.html', {})

@login_required(login_url="/")
def user_vocabulary(request: HttpRequest) -> HttpResponse:
    return render(request, 'user_vocabulary.html', {})
