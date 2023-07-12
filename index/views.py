from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.template import loader

from billing.permissions import is_user_subscription_status_valid

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

def privacy_policy(request: HttpRequest) -> HttpResponse:
    return render(request, 'privacy-policy.html', {})

@login_required(login_url="/")
def onboarding(request: HttpRequest):
    if not is_user_subscription_status_valid(request.user):
        return redirect("/subscription/")
    return render(request, 'onboarding.html', {})

@login_required(login_url="/")
def dashboard(request: HttpRequest) -> HttpResponse:
    if not is_user_subscription_status_valid(request.user):
        return redirect("/subscription/")
    return render(request, 'dashboard.html', {})

@login_required(login_url="/")
def quiz(request: HttpRequest) -> HttpResponse:
    if not is_user_subscription_status_valid(request.user):
        return redirect("/subscription/")
    return render(request, 'quiz.html', {})

@login_required(login_url="/")
def subscription(request: HttpRequest) -> HttpResponse:
    return render(request, 'subscription.html', {})
