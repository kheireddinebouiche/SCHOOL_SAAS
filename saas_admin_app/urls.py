from django.urls import path
from django.views.generic import RedirectView
from .views import (
    saas_dashboard_view, saas_login_view, saas_logout_view, saas_performance_view, 
    saas_logs_view, saas_tenant_detail_view, saas_update_user_view,
    saas_tenant_files_view, saas_file_browser_view, saas_file_serve_view,
    saas_reset_user_password_view, saas_email_config_view, saas_test_email_view,
    saas_toggle_maintenance_view
)

app_name = 'saas_admin_app'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='saas_admin_app:saas_login', permanent=False)),
    path('login/', saas_login_view, name='saas_login'),
    path('logout/', saas_logout_view, name='saas_logout'),
    path('dashboard/', saas_dashboard_view, name='saas_dashboard'),
    path('performance/', saas_performance_view, name='saas_performance'),
    path('logs/', saas_logs_view, name='saas_logs'),
    path('tenant/<int:tenant_id>/', saas_tenant_detail_view, name='saas_tenant_detail'),
    path('tenant/<int:tenant_id>/files/', saas_tenant_files_view, name='saas_tenant_files'),
    path('api/tenant/<int:tenant_id>/user/<int:user_id>/update/', saas_update_user_view, name='saas_update_user'),
    path('api/tenant/<int:tenant_id>/user/<int:user_id>/reset-password/', saas_reset_user_password_view, name='saas_reset_user_password'),
    path('api/tenant/<int:tenant_id>/files/browse/', saas_file_browser_view, name='saas_file_browser'),
    path('api/tenant/<int:tenant_id>/files/serve/<path:file_path>', saas_file_serve_view, name='saas_file_serve'),
    path('settings/email/', saas_email_config_view, name='saas_email_config'),
    path('api/settings/email/test/', saas_test_email_view, name='saas_test_email'),
    path('api/settings/maintenance/toggle/', saas_toggle_maintenance_view, name='saas_toggle_maintenance'),
]
