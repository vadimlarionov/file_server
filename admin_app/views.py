from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("It is Python, not Java")
