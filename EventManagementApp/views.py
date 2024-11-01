from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserRegistrationModel, Event, Booking
from .forms import UserRegistrationForm, UserLoginForm, EventForm
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages

# Create your views here.

#def home(request):
#    return render(request, 'users/home.html')

def register_user(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = UserRegistrationForm()
    return render(request, 'events/register.html', 
                  {'form': form})

def user_login(request):

    if request.user.is_authenticated:
        return redirect('user_profile')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            try:
                users = UserRegistrationModel.objects.get(phone_number=phone_number)
                user = authenticate(username=users.user.username, password=password)

                if user is not None:
                    login(request, user)        
                    return redirect(reverse('user_profile')) 
                else:
                    form.add_error(None, 'Invalid password.')
            except UserRegistrationModel.DoesNotExist:
                form.add_error('phone_number', 'This phone number is not registered.')

    else:
        form = UserLoginForm()

    return render(request, 'events/login.html', {'form': form})

@login_required
def user_profile(request):
    user_pro = get_object_or_404(UserRegistrationModel, user=request.user)
    return render(request, 'events/profile.html', {'user_pro': user_pro})


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    search_query = request.GET.get('search', '')
    events = Event.objects.all()

    user_pro = None
    if request.user.is_authenticated:
        try:
            user_pro = request.user.userregistrationmodel 
        except UserRegistrationModel.DoesNotExist:
            user_pro = None

    # Filter events based on search query
    if search_query:
        events = events.filter(Q(name__icontains=search_query) | Q(date__icontains=search_query) | Q(location__icontains=search_query))

    # Get booked events for authenticated users
    booked_events = Booking.objects.filter(user=request.user) if request.user.is_authenticated else None
    booked_event_ids = [booking.event.id for booking in booked_events] if booked_events else []

    return render(request, 'events/home.html', {
        'events': events,
        'booked_event_ids': booked_event_ids,
        'search_query': search_query,
        'user_pro': user_pro
    })

@login_required
def create_event(request):
    title = "Create Event"
    button = "Create Event"
    user_pro = request.user.userregistrationmodel

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect (reverse('event_list')) 
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', 
                  {'form': form, 
                   'title': title,
                   'button': button,
                   'user_pro': user_pro})

@login_required
def update_event(request, event_id):

    event = get_object_or_404(Event, id=event_id, creator=request.user)
    title = "Update Event"
    button = "Update Event"
    user_pro = request.user.userregistrationmodel

    if event.creator != request.user:
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')  
    else:
        form = EventForm(instance=event)

    return render(request, 'events/create_event.html', 
                  {'form': form, 
                   'event': event,
                   'title': title,
                   'button': button,
                   'user_pro': user_pro})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, creator=request.user)
    user_pro = request.user.userregistrationmodel

    if event.creator != request.user:
        return redirect('event_list')

    if request.method == 'POST':
        event.delete()
        return redirect('event_list')  

    return render(request, 'events/delete_event.html', {'event': event,
                   'user_pro': user_pro})

@login_required
def event_list(request):
    events = Event.objects.all()
    user_pro = request.user.userregistrationmodel
    return render(request, 'events/event_list.html', 
                  {'events': events,
                   'user_pro': user_pro})

@login_required
def booked_events(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'events/booked_events.html', {'bookings': bookings})

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if not event.is_fully_booked():
        Booking.objects.create(user=request.user, event=event)
        event.booked_count += 1
        event.save()
    return redirect('home')

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user.is_authenticated:
        user_pro = request.user.userregistrationmodel
    else:
        user_pro = None
        
    return render(request, 'events/event_detail.html', 
                  {'event': event,
                   'user_pro': user_pro})
