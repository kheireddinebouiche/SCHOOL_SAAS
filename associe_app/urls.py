from django.urls import path
from .views import (
    index, 
    configuration_budget, 
    configuration_structure,
    global_payment_type_list,
    global_payment_type_create,
    global_payment_type_edit,
    global_payment_type_delete,
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
    delete_tenant_payment_type,
    crm_statistics,
    get_crm_stats_api,
    postes_budgetaires_list,
    postes_budgetaire_create,
    postes_budgetaire_edit,
    postes_budgetaire_delete,
    
    user_list,
    user_create,
    user_edit,
    user_delete,
    user_toggle_status,

    budget_campaign_list,
    budget_campaign_instituts,
    budget_campaign_create,
    budget_campaign_activate,
    budget_campaign_delete,
    budget_campaign_review,
    extension_requests_list,
    review_extension,
    budget_campaign_activate,
    sync_payment_types,
    export_payment_categories,
    import_payment_categories,
    export_depenses_categories,
    import_depenses_categories,
    export_postes_budgetaires,
    import_postes_budgetaires,
    update_tenant_type,
    reset_tenant_table,
    tenant_workspace,
    preview_tenant_table_reset,
    delete_tenant,
    delete_orphaned_schema,
    list_orphaned_schemas,
    get_tenant_sync_list,
    sync_single_tenant_view,
    mise_en_route,
    notify_tenants_of_campaign,
    api_mark_saas_notification_read,
    api_mark_all_saas_notifications_read,
    api_delete_saas_notification
)


app_name = 'associe_app'

urlpatterns = [
    path('', index, name='configuration_index'),
    path('mise-en-route/', mise_en_route, name='mise_en_route'),



    # Payment Types
    path('payment-types/', global_payment_type_list, name='global_payment_type_list'),
    path('payment-types/create/', global_payment_type_create, name='global_payment_type_create'),
    path('payment-types/edit/<int:pk>/', global_payment_type_edit, name='global_payment_type_edit'),
    path('payment-types/delete/<int:pk>/', global_payment_type_delete, name='global_payment_type_delete'),
    path('payment-types/sync/', sync_payment_types, name='sync_payment_types'),

    # Payment Categories
    path('payment-categories/', global_payment_category_list, name='global_payment_category_list'),
    path('payment-categories/create/', global_payment_category_create, name='global_payment_category_create'),
    path('payment-categories/edit/<int:pk>/', global_payment_category_edit, name='global_payment_category_edit'),
    path('payment-categories/delete/<int:pk>/', global_payment_category_delete, name='global_payment_category_delete'),
    path('payment-categories/export/', export_payment_categories, name='export_payment_categories'),
    path('payment-categories/import/', import_payment_categories, name='import_payment_categories'),

    # Depenses Categories
    path('depenses-categories/', global_depenses_category_list, name='global_depenses_category_list'),
    path('depenses-categories/create/', global_depenses_category_create, name='global_depenses_category_create'),
    path('depenses-categories/edit/<int:pk>/', global_depenses_category_edit, name='global_depenses_category_edit'),
    path('depenses-categories/delete/<int:pk>/', global_depenses_category_delete, name='global_depenses_category_delete'),
    path('depenses-categories/export/', export_depenses_categories, name='export_depenses_categories'),
    path('depenses-categories/import/', import_depenses_categories, name='import_depenses_categories'),

    # Postes Budgetaires
    path('postes-budgetaires/', postes_budgetaires_list, name='postes_budgetaires_list'),
    path('postes-budgetaires/create/', postes_budgetaire_create, name='postes_budgetaire_create'),
    path('postes-budgetaires/edit/<int:pk>/', postes_budgetaire_edit, name='postes_budgetaire_edit'),
    path('postes-budgetaires/delete/<int:pk>/', postes_budgetaire_delete, name='postes_budgetaire_delete'),
    path('postes-budgetaires/export/', export_postes_budgetaires, name='export_postes_budgetaires'),
    path('postes-budgetaires/import/', import_postes_budgetaires, name='import_postes_budgetaires'),

    # Budget Campaigns
    path('budget-campaigns/', budget_campaign_list, name='budget_campaign_list'),
    path('budget-campaigns/create/', budget_campaign_create, name='budget_campaign_create'),
    path('budget-campaigns/<slug:campaign_slug>/instituts/', budget_campaign_instituts, name='budget_campaign_instituts'),
    path('budget-campaigns/<slug:campaign_slug>/activate/', budget_campaign_activate, name='budget_campaign_activate'),
    path('budget-campaigns/<slug:campaign_slug>/notify/', notify_tenants_of_campaign, name='notify_tenants_of_campaign'),
    path('budget-campaigns/<slug:campaign_slug>/delete/', budget_campaign_delete, name='budget_campaign_delete'),
    path('budget-campaigns/<slug:campaign_slug>/review/<int:institut_id>/', budget_campaign_review, name='budget_campaign_review'),
    
    # Extension Requests
    path('extension-requests/', extension_requests_list, name='extension_requests_list'),
    path('extension-requests/<int:request_id>/', review_extension, name='review_extension'),

    path('sync-categories/', sync_categories_view, name='sync_categories_view'),
    path('tenants/get-sync-list/', get_tenant_sync_list, name='get_tenant_sync_list'),
    path('tenants/sync-single/', sync_single_tenant_view, name='sync_single_tenant_view'),

    # Notifications API
    path('api/notifications/mark-read/', api_mark_saas_notification_read, name='ApiMarkNotificationRead'),
    path('api/notifications/mark-all-read/', api_mark_all_saas_notifications_read, name='ApiMarkAllNotificationsRead'),
    path('api/notifications/delete/', api_delete_saas_notification, name='ApiDeleteNotification'),
    
    # CRM Statistics
    path('crm-statistics/', crm_statistics, name='crm_statistics'),
    path('crm-statistics/api/<int:tenant_id>/', get_crm_stats_api, name='get_crm_stats_api'),

    # User Management
    path('users/', user_list, name='user_list'),
    path('users/create/', user_create, name='user_create'),
    path('users/edit/<int:pk>/', user_edit, name='user_edit'),
    path('users/delete/<int:pk>/', user_delete, name='user_delete'),
    path('users/toggle-status/<int:pk>/', user_toggle_status, name='user_toggle_status'),
    
    # Tenants
    path('tenants/', tenant_data_list, name='tenant_data_list'),
    path('tenants/orphans/', list_orphaned_schemas, name='schema_management'),
    path('tenants/orphans/delete/', delete_orphaned_schema, name='delete_orphaned_schema'),
    path('tenants/workspace/<int:tenant_id>/', tenant_workspace, name='tenant_workspace'),
    path('tenants/delete/<int:tenant_id>/', delete_tenant, name='delete_tenant'),
    path('tenants/update-type/', update_tenant_type, name='update_tenant_type'),
    path('tenants/workspace/<int:tenant_id>/categories/', get_tenant_categories, name='get_tenant_categories'),
    path('tenants/workspace/<int:tenant_id>/purge/', purge_tenant_categories, name='purge_tenant_categories'),
    path('tenants/workspace/<int:tenant_id>/delete-pt/<int:payment_type_id>/', delete_tenant_payment_type, name='delete_tenant_payment_type'),
    path('tenants/workspace/reset-table/', reset_tenant_table, name='reset_tenant_table'),
    path('tenants/workspace/preview-reset/', preview_tenant_table_reset, name='preview_tenant_table_reset'),
]
