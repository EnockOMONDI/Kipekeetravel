from django.contrib import admin
from .models import Event, EventCategory, TicketType, Ticket, EventImage


admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(TicketType)
admin.site.register(Ticket)
admin.site.register(EventImage)
