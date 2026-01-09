from django.shortcuts import render
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
    paginator = Paginator(logs_list, 50) # Show 50 logs per page.
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
    }
    return render(request, 'tenant_folder/crm/logs_list.html', context)
