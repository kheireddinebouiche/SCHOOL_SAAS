from django.shortcuts import render,redirect
from django.http import JsonResponse
from ..models import *
from ..forms import *
from django.contrib import messages
from t_tresorerie.models import *
from t_formations.models import *
from django.db import transaction
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied
from functools import wraps
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.utils.dateformat import format


@login_required(login_url="institut_app:login")
def ApiGeneratePaiementRequest(id_preinscrit):
    pass