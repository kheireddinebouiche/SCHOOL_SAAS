from django.contrib import admin
from django.urls import path,include
from .views import *
from .admin import tenant_admin_site
from django.contrib.auth.views import LoginView, LogoutView
from .api.api import *
from t_etudiants.api.views import get_student_profile_api, get_student_planning_api, get_student_notes_api, get_student_attendance_api, get_student_finances_api, get_student_notifications_api


app_name="app"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Index, name="index"),  
    path('admin_tenant/', tenant_admin_site.urls),
    path('nouveau-compte/', new_tenant, name="nouveau-tenant"),
    path('liste-comptes/', tenant_list, name="tenant_list"),
    
    path('nouveau-utilisateur/', CreateSuperUser, name="CreateSuperUser"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('profile', profile, name="profile"),
    path('nbleads/',NombreLead, name="NombreLead"),
    path('socialEngagement/', socialEngagement, name="socialEngagement"),
    path('configuration/', include('associe_app.urls')),
    path('saas-admin/', include('saas_admin_app.urls')),
    
    path('api/v1/institutes/verify/', verify_institute, name='verify_institute'),
    path('api/v1/students/verify/', verify_student, name='verify_student'),
    path('api/v1/students/login/', login_student, name='login_student'),
    path('api/v1/students/profile/', get_student_profile_api, name='get_student_profile_api'),
    path('api/v1/students/planning/', get_student_planning_api, name='get_student_planning_api'),
    path('api/v1/students/notes/', get_student_notes_api, name='get_student_notes_api'),
    path('api/v1/students/attendance/', get_student_attendance_api, name='get_student_attendance_api'),
    path('api/v1/students/finances/', get_student_finances_api, name='get_student_finances_api'),
    path('api/v1/students/notifications/', get_student_notifications_api, name='get_student_notifications_api'),

    # path('login/',LoginView.as_view(), name="login"),
    # path('logout/',LogoutView.as_view(), name="logout"),

]
