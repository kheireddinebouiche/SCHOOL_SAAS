from django.urls import path
from .views import (
    index, 
    configuration_budget, 
    configuration_structure,
    global_payment_category_list,
    global_payment_category_create,
    global_payment_category_edit,
    global_payment_category_delete,
    global_depenses_category_list,
    global_depenses_category_create,
    global_depenses_category_edit,
    global_depenses_category_delete,
    sync_categories_view,
    tenant_data_list,
    get_tenant_categories,
    purge_tenant_categories,
    crm_statistics,
    get_crm_stats_api,
    postes_budgetaires_list,
    postes_budgetaire_create,
    postes_budgetaire_edit,
    postes_budgetaire_delete
)

urlpatterns = [
    path('', index, name='configuration_index'),
    path('budget/', configuration_budget, name='configuration_budget'),
    path('structure/', configuration_structure, name='configuration_structure'),

    # Tenant Visualization
    path('tenants/', tenant_data_list, name='tenant_data_list'),
    path('tenants/categories/<int:tenant_id>/', get_tenant_categories, name='get_tenant_categories'),
    path('tenants/purge/<int:tenant_id>/', purge_tenant_categories, name='purge_tenant_categories'),
    path('crm-statistics/', crm_statistics, name='crm_statistics'),
    path('crm-statistics/api/<int:tenant_id>/', get_crm_stats_api, name='get_crm_stats_api'),

    # Payment Categories
    path('payment-categories/', global_payment_category_list, name='global_payment_category_list'),
    path('payment-categories/create/', global_payment_category_create, name='global_payment_category_create'),
    path('payment-categories/edit/<int:pk>/', global_payment_category_edit, name='global_payment_category_edit'),
    path('payment-categories/delete/<int:pk>/', global_payment_category_delete, name='global_payment_category_delete'),

    # Depenses Categories
    path('depenses-categories/', global_depenses_category_list, name='global_depenses_category_list'),
    path('depenses-categories/create/', global_depenses_category_create, name='global_depenses_category_create'),
    path('depenses-categories/edit/<int:pk>/', global_depenses_category_edit, name='global_depenses_category_edit'),
    path('depenses-categories/delete/<int:pk>/', global_depenses_category_delete, name='global_depenses_category_delete'),

    # Postes Budgetaires
    path('postes-budgetaires/', postes_budgetaires_list, name='postes_budgetaires_list'),
    path('postes-budgetaires/create/', postes_budgetaire_create, name='postes_budgetaire_create'),
    path('postes-budgetaires/edit/<int:pk>/', postes_budgetaire_edit, name='postes_budgetaire_edit'),
    path('postes-budgetaires/delete/<int:pk>/', postes_budgetaire_delete, name='postes_budgetaire_delete'),

    path('sync-categories/', sync_categories_view, name='sync_categories_view'),
]
