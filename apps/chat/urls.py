from django.urls import path
from apps.chat.views import login, logout, chat_view

urlpatterns = [
    path('chat', chat_view, name='chat'),
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
]

