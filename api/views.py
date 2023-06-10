from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.template import loader

@ensure_csrf_cookie
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/index.html', {})

def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/dashboard.html', {})


def login(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return redirect("/?error=bad_req")
    user = authenticate(username=request.POST["email"], password=request.POST["password"])
    if not user:
        return redirect("/?error=bad_auth")
    else:
        login(request, user)
        return redirect("/dashboard/")
