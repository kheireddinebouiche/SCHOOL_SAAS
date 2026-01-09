from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from t_crm.models import UserActionLog
from django.contrib.auth.models import User

@login_required
def user_action_log_list(request):
    logs_list = UserActionLog.objects.all()

    # Filtering
    user_id = request.GET.get('user')
    action_type = request.GET.get('action_type')
    target_model = request.GET.get('target_model')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if user_id:
        logs_list = logs_list.filter(user_id=user_id)
    if action_type:
        logs_list = logs_list.filter(action_type=action_type)
    if target_model:
        logs_list = logs_list.filter(target_model__icontains=target_model)
    if date_from:
        logs_list = logs_list.filter(created_at__gte=date_from)
    if date_to:
        logs_list = logs_list.filter(created_at__lte=date_to)

    # Pagination
    per_page = request.GET.get('per_page', '25')
    if not per_page.isdigit() or int(per_page) not in [25, 50, 100]:
        per_page = '25'
        
    paginator = Paginator(logs_list, int(per_page))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    users = User.objects.all()
    action_choices = UserActionLog.ACTION_CHOICES

    context = {
        'page_obj': page_obj,
        'users': users,
        'action_choices': action_choices,
        'selected_user': int(user_id) if user_id else None,
        'selected_action': action_type,
        'selected_target': target_model,
        'date_from': date_from,
        'date_to': date_to,
        'per_page': per_page,
    }
    return render(request, 'tenant_folder/crm/logs_list.html', context)

@login_required
def clear_logs(request):
    if not request.user.is_staff:
         messages.error(request, "Vous n'avez pas la permission d'effectuer cette action.")
         return redirect('t_crm:user_action_log_list')
         
    if request.method == 'POST':
        mode = request.POST.get('delete_mode')
        
        if mode == 'all':
            UserActionLog.objects.all().delete()
            messages.success(request, "Tout le journal d'actions a été vidé.")
            
        elif mode == 'older_than':
            date_threshold = request.POST.get('date_threshold')
            if date_threshold:
                count, _ = UserActionLog.objects.filter(created_at__lt=date_threshold).delete()
                messages.success(request, f"{count} entrées antérieures au {date_threshold} ont été supprimées.")
            else:
                messages.error(request, "Veuillez spécifier une date limite.")

        elif mode == 'period':
            date_from = request.POST.get('date_from_delete')
            date_to = request.POST.get('date_to_delete')
            if date_from and date_to:
                 # Add one day to date_to to include the full day
                import datetime
                # Handle potential date parsing if needed, but standard string comparison works for iso dates in filters usually, 
                # though strictly speaking django filter expects datetime objects or strings.
                # Let's rely on standard string format YYYY-MM-DD from HTML input.
                
                # To include the end date fully, we often need to go to next day or use __date lookup.
                # Simplified: use range on dates.
                count, _ = UserActionLog.objects.filter(created_at__range=[date_from, date_to + ' 23:59:59']).delete()
                messages.success(request, f"{count} entrées supprimées sur la période.")
            else:
                messages.error(request, "Veuillez spécifier une période complète.")
        
    return redirect('t_crm:user_action_log_list')
