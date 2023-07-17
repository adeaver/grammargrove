from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login as login_request
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.template import loader

from billing.permissions import is_user_subscription_status_valid

@ensure_csrf_cookie
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', {
        "title": "GrammarGrove"
    })

def login(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect("/?error=bad_req")
    user = authenticate(request, username=request.POST["email"], password=request.POST["password"])
    if not user:
        return redirect("/?error=bad_auth")
    else:
        login_request(request, user)
        return redirect("/dashboard/")

def privacy_policy(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', {
        "title": "GrammarGrove | Privacy Policy"
    })

@login_required(login_url="/")
def onboarding(request: HttpRequest):
    if not is_user_subscription_status_valid(request.user):
        return redirect("/subscription/")
    return render(request, 'index.html', {
        "title": "GrammarGrove | Onboarding"
    })

@login_required(login_url="/")
def dashboard(request: HttpRequest) -> HttpResponse:
    if not is_user_subscription_status_valid(request.user):
        return redirect("/subscription/")
    return render(request, 'index.html', {
        "title": "GrammarGrove | Dashboard"
    })

@login_required(login_url="/")
def preferences(request: HttpRequest) -> HttpResponse:
    if not is_user_subscription_status_valid(request.user):
        return redirect("/subscription/")
    return render(request, 'index.html', {
        "title": "GrammarGrove | Preferences"
    })

@login_required(login_url="/")
def quiz(request: HttpRequest) -> HttpResponse:
    if not is_user_subscription_status_valid(request.user):
        return redirect("/subscription/")
    return render(request, 'index.html', {
        "title": "GrammarGrove | Quiz"
    })

@login_required(login_url="/")
def subscription(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', {
        "title": "GrammarGrove | Subscription Management"
    })
