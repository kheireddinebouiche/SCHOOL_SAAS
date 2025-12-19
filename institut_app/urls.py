from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from .f_views.entreprise import *

app_name="institut_app"

urlpatterns = [
    
    path('',Index, name="index"),
   
    path('login/',login_view, name="login"),
    path('register/', register, name="register"),
    path('logout/',logout_view, name="logout"),
    path('blocked/', ShowBlockedConnexion, name="ShowBlockedConnexion"),
    path('ApiLoadEntrepriseLogos',ApiLoadEntrepriseLogos, name="ApiLoadEntrepriseLogos"),
    path('ApiUpdateEntrepriseLogos', ApiUpdateEntrepriseLogos,name="ApiUpdateEntrepriseLogos"),

    path('nouvelle-entreprise/', NewEntreprise, name="new_entreprise"),
    path('details-entreprise/<int:pk>/', detailsEntreprise, name="details_entreprise"),
    path('liste-des-entreprise/', ListeEntreprises, name="liste_entreprise"),
    path('modification-entreprise/<int:id>/', ModifierEntreprise, name="modifier_entreprise"),
    #path('update-entreprise/', ApiUpdateEntreprise, name="update_entreprise"),

    path('utilisateurs/',UsersListePage, name="UsersListePage"),
    path('ApiListeUsers',ApiListeUsers,name="ApiListeUsers"),
    path('ApiGetDetailsProfile', ApiGetDetailsProfile, name="ApiGetDetailsProfile"),
    path('ApiCreateProfile', ApiCreateProfile, name="ApiCreateProfile"),
    path('ApiDeactivateUser', ApiDeactivateUser, name="ApiDeactivateUser"),
    path('ApiActivateUser', ApiActivateUser, name="ApiActivateUser"),

    path('group-list/', ListGroupePage, name="ListGroupePage"),
    path('ApilistGroupe', ApilistGroupe, name="ApilistGroupe"),

    path('NewCustomGroupe', NewCustomGroupe, name="NewCustomGroupe"),
    path('ApiGetGroupFrom', ApiGetGroupFrom, name="ApiGetGroupFrom"),
    path('ApiSaveGroup', ApiSaveGroup, name="ApiSaveGroup"),
    path('ApiGetGroupeDetails', ApiGetGroupeDetails, name="ApiGetGroupeDetails"),
    path('ApiGetUpdateGroupForm', ApiGetUpdateGroupForm, name="ApiGetUpdateGroupForm"),
    path('ApiDeleteGroup', ApiDeleteGroup, name="ApiDeleteGroup"),

    path('ApiGetNewUserForm', ApiGetNewUserForm, name="ApiGetNewUserForm"),
    path('ApiSaveUser', ApiSaveUser, name="ApiSaveUser"),
    path('ApiGetUserDetails', ApiGetUserDetails, name="ApiGetUserDetails"),
    path('modification-details-utilisateur/<int:pk>/', PageUpdateUserDetails, name="PageUpdateUserDetails"),
    path('ApiCheckUsernameDisponibility',ApiCheckUsernameDisponibility, name="ApiCheckUsernameDisponibility"),

    path('profile/',GetMyProfile, name="profile"),
    path('mise-a-jour-profile/', UpdateMyProfile, name="UpdateProfile"),


    path('ApiLoadEntrepriseData', ApiLoadEntrepriseData , name="ApiLoadEntrepriseData"),
    path('ApiUpdateEntrepriseData', ApiUpdateEntrepriseData , name="ApiUpdateEntrepriseData"),
    
    path('ApiSaveBankAccount', ApiSaveBankAccount, name="ApiSaveBankAccount"),
    path('ApiListeBanckAccountEntreprise', ApiListeBanckAccountEntreprise, name="ApiListeBanckAccountEntreprise"),
    path('ApiLoadBankAccountDetails', ApiLoadBankAccountDetails, name="ApiLoadBankAccountDetails"),
    path('ApiArchiveBankAccount',ApiArchiveBankAccount, name="ApiArchiveBankAccount"),


    path('tableau-de-bord/finance/', FinanceDashboard, name="FinanceDashboard"),
    path('ApiFinanceKPIs', ApiFinanceKPIs, name="ApiFinanceKPIs"),
    path('error-404/', Error404, name="Error404"),

    path('administration/modules/liste/', ModulesPages, name="ModulesPages"),
    path('ApiListeModules', ApiListeModules, name="ApiListeModules"),
    path('ApiGetModuleDetails',ApiGetModuleDetails, name="ApiGetModuleDetails"),
    path('ApiDeleteModule', ApiDeleteModule, name="ApiDeleteModule"),
    path('ApiAddModule', ApiAddModule, name="ApiAddModule"),
    path('ApiChangeModuleStatus', ApiChangeModuleStatus, name="ApiChangeModuleStatus"),
    path('ApiUpdateModule', ApiUpdateModule, name="ApiUpdateModule"),

    path('administration/roles/liste', roles_page, name="roles_page"),
    path('ApiListeRoles',ApiListeRoles, name="ApiListeRoles"),
    path('ApiDeleteRole', ApiDeleteRole, name="ApiDeleteRole"),
    path('ApiChangeRoleStatus', ApiChangeRoleStatus, name="ApiChangeRoleStatus"),
    path('ApiAddRole', ApiAddRole, name="ApiAddRole"),
    path('ApiUpdateRole', ApiUpdateRole, name="ApiUpdateRole"),
    path('ApiGetRoleDetails', ApiGetRoleDetails, name="ApiGetRoleDetails"),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)