from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Reminder, Message, ChatGroup
from django.db.models import Q
import json
from django.utils.dateparse import parse_datetime

@login_required
def calendar_view(request):
    users = User.objects.exclude(id=request.user.id)
    
    # Calculate stats
    reminders = Reminder.objects.filter(
        Q(user=request.user) | Q(participants=request.user)
    ).distinct()
    
    total = reminders.count()
    completed = reminders.filter(is_completed=True).count()
    pending = total - completed
    
    context = {
        'users': users,
        'stats': {
            'total': total,
            'completed': completed,
            'pending': pending
        }
    }
    return render(request, 'tenant_folder/communication/calendar.html', context)

@login_required
def reminder_api_list(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    # Filter reminders where user is owner OR participant
    reminders = Reminder.objects.filter(
        Q(user=request.user) | Q(participants=request.user)
    ).distinct()
    
    if start and end:
        reminders = reminders.filter(start_time__gte=start, start_time__lte=end)
    
    events = []
    for r in reminders:
        is_owner = r.user == request.user
        base_class = r.category
        owner_class = 'event-owner' if is_owner else 'event-invited'
        status_class = 'event-completed' if r.is_completed else 'event-pending'
        
        events.append({
            'id': r.id,
            'title': r.title,
            'start': r.start_time.isoformat(),
            'end': r.end_time.isoformat() if r.end_time else None,
            'description': r.description,
            'className': f"{base_class} {owner_class} {status_class}",
            'extendedProps': {
                'is_completed': r.is_completed,
                'category': r.category,
                'is_owner': is_owner,
                'participants': list(r.participants.values_list('id', flat=True))
            },
            # Visual cue for shared events if needed
            'borderColor': '#000' if not is_owner else None
        })
    return JsonResponse(events, safe=False)

@login_required
def reminder_api_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reminder = Reminder.objects.create(
            user=request.user,
            title=data.get('title'),
            description=data.get('description'),
            category=data.get('category', 'bg-primary'),
            start_time=parse_datetime(data.get('start')),
            end_time=parse_datetime(data.get('end')) if data.get('end') else None
        )
        participant_ids = data.get('participants', [])
        if participant_ids:
            reminder.participants.set(participant_ids)
        return JsonResponse({'status': 'success', 'id': reminder.id})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def reminder_api_update(request, pk):
    # Allow update if owner 
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    if request.method == 'POST':
        data = json.loads(request.body)
        reminder.title = data.get('title', reminder.title)
        reminder.description = data.get('description', reminder.description)
        reminder.category = data.get('category', reminder.category)
        if data.get('start'):
            reminder.start_time = parse_datetime(data.get('start'))
        if data.get('end'):
            reminder.end_time = parse_datetime(data.get('end'))
        reminder.is_completed = data.get('is_completed', reminder.is_completed)
        
        participant_ids = data.get('participants')
        if participant_ids is not None: # Check for None to allow empty list clearing
            reminder.participants.set(participant_ids)
            
        reminder.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def reminder_api_delete(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    if request.method == 'POST':
        reminder.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def messages_view(request):
    # Get all users the current user has chatted with
    sent_to = Message.objects.filter(sender=request.user, group__isnull=True).values_list('receiver', flat=True)
    received_from = Message.objects.filter(receiver=request.user, group__isnull=True).values_list('sender', flat=True)
    contact_ids = set(list(sent_to) + list(received_from))
    
    contacts = User.objects.filter(id__in=contact_ids).exclude(id=request.user.id)
    all_users = User.objects.exclude(id=request.user.id)
    
    # Get user's groups
    groups = ChatGroup.objects.filter(members=request.user)
    
    return render(request, 'tenant_folder/communication/messages.html', {
        'contacts': contacts,
        'all_users': all_users,
        'groups': groups
    })

@login_required
def conversation_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    # Mark messages as read
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    return render(request, 'tenant_folder/communication/conversation_partial.html', {
        'other_user': other_user,
        'messages': messages,
        'is_group': False
    })

@login_required
def group_conversation_view(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id, members=request.user)
    messages = group.messages.all().order_by('timestamp')
    
    return render(request, 'tenant_folder/communication/conversation_partial.html', {
        'group': group,
        'messages': messages,
        'is_group': True
    })

@login_required
def create_group_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        member_ids = data.get('members', [])
        
        if not name:
             return JsonResponse({'status': 'error', 'message': 'Le nom du groupe est requis'}, status=400)
             
        group = ChatGroup.objects.create(
            name=name,
            admin=request.user
        )
        group.members.add(request.user) # Add creator
        if member_ids:
            group.members.add(*member_ids)
            
        return JsonResponse({
            'status': 'success', 
            'group': {
                'id': group.id,
                'name': group.name
            }
        })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def send_message_api(request):
    if request.method == 'POST':
        # Check content type to decide how to parse data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            receiver_id = data.get('receiver_id')
            group_id = data.get('group_id')
            content = data.get('content')
            file = None
        else:
            # Assume multipart/form-data
            receiver_id = request.POST.get('receiver_id')
            group_id = request.POST.get('group_id')
            content = request.POST.get('content')
            file = request.FILES.get('file')
        
        if not receiver_id and not group_id:
            return JsonResponse({'status': 'error', 'message': 'Missing receiver_id or group_id'}, status=400)
            
        if not content and not file:
            return JsonResponse({'status': 'error', 'message': 'Message cannot be empty'}, status=400)
        
        sender = request.user
        msg = Message(sender=sender, content=content if content else "", file=file)
        
        if group_id:
            group = get_object_or_404(ChatGroup, id=group_id, members=request.user)
            msg.group = group
        else:
            receiver = get_object_or_404(User, id=receiver_id)
            msg.receiver = receiver
            
        msg.save()
        
        response_data = {
            'status': 'success', 
            'message_id': msg.id,
            'timestamp': msg.timestamp.strftime('%H:%M'),
            'sender_name': sender.username # Useful for group chat
        }
        
        if msg.file:
            response_data['file_url'] = msg.file.url
            response_data['file_name'] = msg.file.name.split('/')[-1]
            
        return JsonResponse(response_data)
    return JsonResponse({'status': 'error'}, status=400)
