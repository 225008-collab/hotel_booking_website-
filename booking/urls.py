from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.book_room, name='book_room'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]

