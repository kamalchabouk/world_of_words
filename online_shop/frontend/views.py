from django.shortcuts import render

# Create your views here.
from typing import Any
from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render
import json
import requests
from django.shortcuts import get_object_or_404


class HomeView(TemplateView):
    template_name = "home.html"
