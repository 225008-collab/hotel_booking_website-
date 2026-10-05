from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Room, Booking
from .forms import BookingForm, RegisterForm
from django.contrib.auth import login

def room_list(request):
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    capacity = request.GET.get('capacity')
    rooms = Room.objects.all()

    if capacity:
        rooms = rooms.filter(capacity__gte=capacity)

    if check_in and check_out:
        rooms = rooms.exclude(
            Q(bookings__check_in__lt=check_out) &
            Q(bookings__check_out__gt=check_in)
        )

    return render(request, 'booking/room_list.html', {'rooms': rooms})

@login_required
def book_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, room=room)
        if form.is_valid():
            data = form.cleaned_data
            Booking.objects.create(
                user=request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out'],
                guests=data['guests'],
            )
            messages.success(request, 'Booking confirmed!')
            return redirect('my_bookings')
    else:
        form = BookingForm(room=room)
    return render(request, 'booking/book_room.html', {'room': room, 'form': form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('room')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('room_list')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})
