from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.register_user, name='register_user'),
    path('profile/', views.user_profile, name='user_profile'),
    path('logout/', views.user_logout, name = 'user_logout'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/', views.event_list, name='event_list'),
    path('event/create/', views.create_event, name='create_event'),
    path('event/<int:event_id>/update/', views.update_event, name='update_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('booked_events/', views.booked_events, name='booked_events'),
    path('book_event/<int:event_id>/', views.book_event, name='book_event'),
]