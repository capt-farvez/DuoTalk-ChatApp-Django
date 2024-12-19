from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.db.models import Q
from .models import Message


def login(request):
    
    if not request.user.is_authenticated:      
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['psw']
            
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                if user.check_password(password):
                    auth_login(request, user)
                    return redirect('/chat')
                else:
                    messages.error(request, "Incorrect password!")
            else:
                messages.error(request, "Unknown username, Please try Again!")
                return redirect('/login')

        return render(request, 'user_auth/login.html')
    
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return render(request, 'user_auth/logout.html')


@login_required
def chat_view(request):
    user = request.user
    
    # Ensure the current user is allowed to chat
    if not user.username in ["user@1", "user@2"]:
        return redirect('/')  # Redirect unauthorized users
    
    # Determine the other user based on the current user
    other_user_username = "user@1" if user.username == "user@2" else "user@2"
    other_user = User.objects.get(username=other_user_username)

    # Fetch the latest 6 messages between the current user and the other user
    messages = Message.objects.filter(
        Q(sender=user, receiver=other_user) | Q(sender=other_user, receiver=user)
    ).order_by('-timestamp')[:20]  # Latest 20 messages
    
    # Get the latest message to show with the reply form
    latest_message = messages.first() if messages.exists() else None

    # Handle new message submission
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=user, receiver=other_user, content=content)
            return redirect('chat')  # Redirect to the same page to update messages

    return render(request, 'chat/chat.html', {
        'messages': messages,
        'other_user': other_user,
        'latest_message': latest_message
    })


# User paginators for chat messages

# @login_required
# def chat_view(request):
#     user = request.user
    
#     # Ensure the current user is allowed to chat
#     if not user.username in ["user@1", "user@2"]:
#         return redirect('/')  # Redirect unauthorized users
    
#     # Determine the other user based on the current user
#     other_user_username = "user@1" if user.username == "user@2" else "user@2"
#     other_user = User.objects.get(username=other_user_username)

#     # Fetch messages between the current user and the other user
#     messages = Message.objects.filter(
#         Q(sender=user, receiver=other_user) | Q(sender=other_user, receiver=user)
#     ).order_by('timestamp')

#     # Pagination setup: Show 6 messages at a time
#     paginator = Paginator(messages, 6)
#     page_number = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_number)

#     # Get the latest message to show with the reply form
#     latest_message = messages.last() if messages.exists() else None

#     # Handle new message submission
#     if request.method == "POST":
#         content = request.POST.get('content')
#         if content:
#             Message.objects.create(sender=user, receiver=other_user, content=content)
#             return redirect('chat')  # Redirect to the same page to update messages

#     return render(request, 'chat/chat.html', {
#         'messages': page_obj,
#         'other_user': other_user,
#         'latest_message': latest_message
#     })
