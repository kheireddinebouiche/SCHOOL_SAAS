from django.contrib import admin
from django.urls import path,include
from .views import *

app_name="t_timetable"

urlpatterns = [
    
    path('liste', ListeDesEmploie, name="ListeDesEmploie"),
    path('creation/', CreateTimeTable, name="CreateTimeTable"),
    path('details/emploie/<int:pk>/',timetable_view, name="timetable_view"),
    path('modifications/emploie/<int:pk>/', timetable_edit, name="timetable_edit"),
    path('configuration/emploie/<int:pk>/', timetable_configure, name="timetable_configure"),

    ### APIS ###
    path('save_day', save_day, name="save_day"),
    path('update_day', update_day, name="update_day"),
    path('delete_day', delete_day, name="delete_day"),


    path('save_horaire', save_horaire, name="save_horaire"),
    path('update_horaire', update_horaire, name="update_horaire"),
    path('delete_horaire', delete_horaire, name="delete_horaire"),



]