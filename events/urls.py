from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Event Views
    path('', views.EventListView.as_view(), name='event_list'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('event/<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event/<slug:slug>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('event/<slug:slug>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    
    # Ticket Management
    path('event/<int:event_id>/ticket-type/create/', views.create_ticket_type, name='create_ticket_type'),
    path('ticket-type/<int:ticket_type_id>/purchase/', views.purchase_ticket, name='purchase_ticket'),
    path('ticket/<int:ticket_id>/confirmation/', views.purchase_confirmation, name='purchase_confirmation'),
    
    # User Dashboard
    path('my-events/', views.my_events, name='my_events'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),

  
]