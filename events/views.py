from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.db.models import Q
from .models import Event, EventCategory, TicketType, Ticket, EventImage, EventsLaunchNotification
from .forms import EventForm, TicketTypeForm, TicketPurchaseForm, EventImageForm, EventSearchForm, LaunchNotificationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.views.generic import TemplateView

import logging

logger = logging.getLogger(__name__)

# In views.py


class EventOrganizersView(TemplateView):
    template_name = 'users/events/event_organizers.html'

class EventListView(ListView):
    model = Event
    template_name = 'users/events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        queryset = Event.objects.filter(status='published')
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        
        if category:
            queryset = queryset.filter(category__slug=category)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(venue__icontains=search) |
                Q(city__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['search_form'] = EventSearchForm(self.request.GET)
            context['categories'] = EventCategory.objects.all()
            context['featured_events'] = Event.objects.filter(
                is_featured=True, 
                status='published'
            )[:3]
            return context

    def get_queryset(self):
        queryset = Event.objects.filter(status='published')
        form = EventSearchForm(self.request.GET)
        
        if form.is_valid():
            if form.cleaned_data.get('search'):
                queryset = queryset.filter(
                    Q(title__icontains=form.cleaned_data['search']) |
                    Q(description__icontains=form.cleaned_data['search'])
                )
            if form.cleaned_data.get('category'):
                queryset = queryset.filter(category=form.cleaned_data['category'])
            if form.cleaned_data.get('date_from'):
                queryset = queryset.filter(start_date__gte=form.cleaned_data['date_from'])
            if form.cleaned_data.get('date_to'):
                queryset = queryset.filter(end_date__lte=form.cleaned_data['date_to'])
            if form.cleaned_data.get('city'):
                queryset = queryset.filter(city__icontains=form.cleaned_data['city'])
                
        return queryset

class EventDetailView(DetailView):
    model = Event
    template_name = 'users/events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket_types'] = self.object.ticket_types.all()
        context['related_events'] = Event.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'users/events/event_form.html'
    form_class = EventForm

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Event created successfully!')
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    template_name = 'users/events/event_form.html'
    form_class = EventForm

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer

    def form_valid(self, form):
        messages.success(self.request, 'Event updated successfully!')
        return super().form_valid(form)

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'users/events/event_confirm_delete.html'
    success_url = reverse_lazy('events:my_events')

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer

@login_required
def create_ticket_type(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    
    if request.method == 'POST':
        form = TicketTypeForm(request.POST)
        if form.is_valid():
            ticket_type = form.save(commit=False)
            ticket_type.event = event
            ticket_type.save()
            messages.success(request, 'Ticket type created successfully!')
            return redirect('events:event_detail', slug=event.slug)
    else:
        form = TicketTypeForm()
    
    return render(request, 'users/events/ticket_type_form.html', {
        'form': form,
        'event': event
    })

@login_required
def purchase_ticket(request, ticket_type_id):
    ticket_type = get_object_or_404(TicketType, id=ticket_type_id)
    
    if request.method == 'POST':
        form = TicketPurchaseForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            # Validate ticket availability
            if quantity > ticket_type.tickets_remaining():
                messages.error(request, 'Not enough tickets available!')
                return redirect('events:event_detail', slug=ticket_type.event.slug)
            
            ticket = form.save(commit=False)
            ticket.ticket_type = ticket_type
            ticket.purchaser = request.user
            ticket.unit_price = ticket_type.price
            ticket.total_price = ticket_type.price * quantity
            ticket.save()
            
            messages.success(request, 'Ticket purchased successfully!')
            return redirect('events:purchase_confirmation', ticket_id=ticket.id)
    else:
        form = TicketPurchaseForm()
    
    return render(request, 'users/events/purchase_ticket.html', {
        'form': form,
        'ticket_type': ticket_type
    })

@login_required
def my_events(request):
    events = Event.objects.filter(organizer=request.user)
    return render(request, 'users/events/my_events.html', {'events': events})

@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(purchaser=request.user)
    return render(request, 'users/events/my_tickets.html', {'tickets': tickets})

def purchase_confirmation(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, purchaser=request.user)
    return render(request, 'users/events/purchase_confirmation.html', {'ticket': ticket})



def notify_launch(request):
    if request.method == 'POST':
        form = LaunchNotificationForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                
                # Save the email to database
                notification = form.save()
                
                # Setup SMTP connection
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                
                # First send the user confirmation email
                try:
                    user_msg = MIMEMultipart('alternative')
                    user_msg['From'] = "DEDE EXPEDITIONS <dedeexpeditions@gmail.com>"
                    user_msg['To'] = email
                    user_msg['Subject'] = "Events Launch Notification Confirmation"
                    
                    user_html = f"""
                    <html>
                    <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                            .header {{ background-color: #f8f9fa; padding: 20px; text-align: center; }}
                            .content {{ padding: 20px; }}
                            .button {{ 
                                background-color: #007bff;
                                color: white;
                                padding: 10px 20px;
                                text-decoration: none;
                                border-radius: 5px;
                                display: inline-block;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <h2>Thank You for Your Interest!</h2>
                            </div>
                            <div class="content">
                                <p>Dear valued customer,</p>
                                <p>Thank you for signing up to be notified about the launch of our Events feature at DEDE EXPEDITIONS.</p>
                                <p>We'll send you an email as soon as our Events feature goes live, so you can be among the first to:</p>
                                <ul>
                                    <li>Discover exciting events</li>
                                    <li>Book tickets directly through our platform</li>
                                    <li>Get exclusive early access to special events</li>
                                </ul>
                                <p>Best regards,<br>The DEDE EXPEDITIONS Team</p>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    
                    user_msg.attach(MIMEText(user_html, 'html'))
                    
                    # Send user email
                    print(f"Attempting to send email to user: {email}")  # Debug print
                    s.send_message(user_msg)
                    print("User email sent successfully")  # Debug print
                    
                except Exception as user_email_error:
                    print(f"Error sending user email: {str(user_email_error)}")  # Debug print
                    raise  # Re-raise the exception to be caught by the outer try block
                
                # Then send the admin notification
                try:
                    admin_msg = MIMEMultipart('alternative')
                    admin_msg['From'] = "DEDE EXPEDITIONS <dedeexpeditions@gmail.com>"
                    admin_msg['To'] = "events@dedeexpeditions.com"
                    admin_msg['Reply-To'] = email  # Add reply-to header
                    admin_msg['Subject'] = "New Events Launch Notification Signup"
                    
                    admin_html = f"""
                    <html>
                    <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                            .header {{ background-color: #f8f9fa; padding: 20px; }}
                            .content {{ padding: 20px; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <h2>New Launch Notification Signup</h2>
                            </div>
                            <div class="content">
                                <p>A new user has signed up for Events Launch notification:</p>
                                <p><strong>Email:</strong> {email}</p>
                                <p><strong>Time:</strong> {timezone.now()}</p>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    
                    admin_msg.attach(MIMEText(admin_html, 'html'))
                    
                    # Send admin email
                    s.send_message(admin_msg)
                    
                except Exception as admin_email_error:
                    print(f"Error sending admin email: {str(admin_email_error)}")  # Debug print
                    # Continue even if admin email fails
                
                finally:
                    # Close SMTP connection
                    s.quit()
                
                messages.success(request, "Thank you! We'll notify you when we launch.")
                return redirect('events:event_list')
                
            except Exception as e:
                print(f"Error in notify_launch: {str(e)}")  # Debug print
                messages.error(request, "There was an error sending the confirmation email. Please try again later.")
                
    else:
        form = LaunchNotificationForm()
    
    return render(request, 'users/events/notify_launch.html', {'form': form})