from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from discord_app.forms import RoomForm,UserForm,MyUserCreationForm
from django.db.models import Q
from django.contrib.auth import get_user_model

from django.contrib import messages

from django.contrib.auth import authenticate,login,logout
# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            messages.error(request, "Invalid Email")
            return redirect('login') 
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Email or password is incorrect")

    context = {'page': page}
    return render(request, 'login_register.html', context)

def logoutuser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()
    
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()  
            user.save()
            login(request, user) 
            return redirect('home')  
        else:
            messages.error(request, "There was an error with your registration.")
    
    context = {'form': form}
    return render(request, 'login_register.html', context)  

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q) 
        )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages= Message.objects.filter(Q(room__topic__name__icontains = q))

    context = {'rooms':rooms,'topics':topics ,'room_count':room_count ,'room_messages':room_messages}
    return render(request , 'HomePage.html',context)

@login_required(login_url = 'loginPage')
def room(request ,pk):
    room= Room.objects.get(id = pk )
    roommessages = room.message_set.all()
    participants = room.participants.all()
    

    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room' ,pk = room.id)

    context = {'room':room ,'roommessages':roommessages ,'participants':participants}

    return render(request, 'Room.Html',context)

def userProfile(request,pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context ={'user':user,'rooms':rooms ,'room_messages':room_messages,'topics':topics}
    return render (request, 'profile.html',context)

@login_required(login_url = 'loginPage')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        
        return redirect('home')
    context = {'form':form ,'topics':topics}
    return render(request ,'room_form.html' ,context)

@login_required(login_url = 'loginPage')
def updateRoom(request,pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You are not allowed")

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('home')



    context = {'form':form ,'topics':topics ,'room':room}
    return render(request ,'room_form.html' ,context)

@login_required(login_url = 'loginPage')
def deleteRoom(request ,pk):
    room = Room.objects.get(id = pk)
    
    if request.user != room.host:
        return HttpResponse("You are not allowed")
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render (request ,'delete.html',{'obj':room})

@login_required(login_url = 'loginPage')
def deleteMessage(request ,pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user :
        return HttpResponse("You are not allowed")
    
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render (request ,'delete.html',{'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userProfile',pk = user.id)
    context ={'form':form}
    return render(request ,'update_user.html',context)

@login_required(login_url = 'loginPage')
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains = q)
    return render(request, 'topics.html',{'topics':topics})

@login_required(login_url = 'loginPage')
def activityPage(request):
    room_messages = Message.objects.all()
    return render(request,'component_activity.html',{'room_messages':room_messages})