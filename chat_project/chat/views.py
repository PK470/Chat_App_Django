from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from core.models import Message
from django.db.models import Q
from datetime import datetime 


from datetime import datetime
from django.utils import timezone  # Import timezone to handle timezone-aware datetime

@login_required
def chat_room(request, room_name):
    search_query = request.GET.get('search', '') 
    User = get_user_model()
    users = User.objects.exclude(id=request.user.id) 
    chats = Message.objects.filter(
    (Q(sender__email=request.user.email) & Q(receiver__email=room_name)) |
    (Q(receiver__email=request.user.email) & Q(sender__email=room_name))
)


    if search_query:
        chats = chats.filter(Q(content__icontains=search_query))  

    chats = chats.order_by('timestamp') 
    user_last_messages = []

    for user in users:
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()

        
        if last_message and last_message.timestamp:
            last_message_timestamp = last_message.timestamp
        else:
            last_message_timestamp = timezone.make_aware(datetime.min)

        user_last_messages.append({
            'user': user,
            'last_message': last_message,
            'last_message_timestamp': last_message_timestamp
        })


    user_last_messages.sort(
        key=lambda x: x['last_message_timestamp'],
        reverse=True
    )

    return render(request, 'chat.html', {
        'room_name': room_name,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'search_query': search_query 
    })
