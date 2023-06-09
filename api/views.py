from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader

def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/index.html', {})
