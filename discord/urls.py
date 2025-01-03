"""
URL configuration for discord project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from discord_app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', loginPage ,name='loginPage'),
    path('logout/', logoutuser ,name='logoutuser'),
    path('register/', registerPage ,name='registerPage'),

    path('', home ,name='home'),
    path('room/<str:pk>/', room ,name='room'),
    path('profile/<str:pk>/', userProfile ,name='userProfile'),
    path('create_room/', create_room ,name='create_room'),
    path('update_room/<str:pk>/', updateRoom ,name='updateRoom'),
    path('delete_room/<str:pk>/', deleteRoom ,name='deleteRoom'),

    path('delete_message/<str:pk>/', deleteMessage ,name='deleteMessage'),
    path('update_user/', updateUser ,name='updateUser'),

     path('topics/', topicsPage ,name='topics'),
     path('activity/', activityPage ,name='activity'),

     path('api/',include('discord_app.api.urls'))
]

urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)