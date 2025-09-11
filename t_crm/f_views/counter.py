from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
from ..models import *
from django.db import transaction
from django.utils.dateformat import format

@login_required(login_url="institut_app:login")
def ApiUpdateVisisteCounter(request):
    pass

@login_required(login_url="institut_app:login")
def ApiUpdatePhoneCallCounter(request):
    pass


