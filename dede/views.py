from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.db.models import Avg
from .models import Destination, Tour, Review
from django.views.generic.edit import CreateView
from .models import Tour, Booking, DayTrip, DayTripBooking
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from events.models import EventCategory
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.exceptions import ValidationError


# Add this view function




class HomeView(ListView):
    model = Tour
    template_name = 'users/dede/index.html'
    context_object_name = 'tours'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'featured_tours': Tour.objects.filter(is_featured=True)[:6],
            'top_tours': Tour.objects.filter(rating__gte=4.5)[:6],
            'popular_destinations': Destination.objects.all()[:6],
            'event_categories': EventCategory.objects.all(),
            'featured_daytrips': DayTrip.objects.filter(
                is_featured=True,
                date__gte=timezone.now().date()
            )[:4],  # Show only upcoming featured day trips
            'today': timezone.now().date(),
        })
        return context



class DayTripListView(ListView):
    model = DayTrip
    template_name = 'users/dede/daytrip_list.html'
    context_object_name = 'daytrips'
    paginate_by = 9

    def get_queryset(self):
        # Show only upcoming daytrips
        return DayTrip.objects.filter(
            date__gte=timezone.now().date()
        ).order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_daytrips'] = DayTrip.objects.filter(
            is_featured=True,
            date__gte=timezone.now().date()
        )[:6]
        return context

class DayTripDetailView(DetailView):
    model = DayTrip
    template_name = 'users/dede/daytrip_detail.html'
    context_object_name = 'daytrip'
    slug_url_kwarg = 'daytrip_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get next 3 upcoming daytrips for recommendations
        context['upcoming_daytrips'] = DayTrip.objects.filter(
            date__gte=timezone.now().date()
        ).exclude(
            id=self.object.id
        ).order_by('date')[:3]
        return context

def send_daytrip_confirmation_email(booking):
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        msg = MIMEMultipart('alternative')
        msg['From'] = "DEDE TOURS TRAVEL <novustellke@gmail.com>"
        msg['To'] = booking.email
        msg['Subject'] = f"Day Trip Booking Confirmation - {booking.booking_reference}"

        # Create activities list for email if any were selected
        activities_html = ""
        if booking.optional_activities.exists():
            activities_html = """
            <div class="booking-details" style="margin-top: 20px;">
                <h3>Optional Activities Booked:</h3>
                <ul>
            """
            for activity in booking.optional_activities.all():
                activities_html += f"<li>{activity.name} - KES {activity.price} per person</li>"
            activities_html += "</ul></div>"

        email_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Day Trip Booking Confirmation</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333333;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    text-align: center;
                    padding: 20px 0;
                    background-color: #f8f9fa;
                }}
                .logo {{
                    max-width: 200px;
                    height: auto;
                }}
                .content {{
                    padding: 20px 0;
                }}
                .booking-details {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    background-color: #f8f9fa;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <img src="https://kipekeetravel.onrender.com/static/assets3/img/logo/dedelogo1.png" alt="DEDE TOURS TRAVEL" class="logo">
                </div>
                
                <div class="content">
                    <h2>Day Trip Booking Confirmation</h2>
                    <p>Dear {booking.full_name},</p>
                    
                    <p>Thank you for booking your day trip with DEDE TOURS TRAVEL! We're excited to have you join us for {booking.daytrip.name}.</p>
                    
                    <div class="booking-details">
                        <h3>Booking Details:</h3>
                        <p><strong>Booking Reference:</strong> {booking.booking_reference}</p>
                        <p><strong>Day Trip:</strong> {booking.daytrip.name}</p>
                        <p><strong>Date:</strong> {booking.daytrip.date}</p>
                        <p><strong>Pickup Time:</strong> {booking.daytrip.pickup_time}</p>
                        <p><strong>Pickup Location:</strong> {booking.daytrip.pickup_location}</p>
                        <p><strong>Number of People:</strong> {booking.number_of_people}</p>
                        <p><strong>Total Price:</strong> KES {booking.total_price}</p>
                    </div>
                    
                    {activities_html}
                    
                    <p>Your booking status is currently <strong>pending</strong>. Our team will contact you shortly regarding payment and final confirmation.</p>
                    
                    <p>If you have any questions, please contact us with your booking reference: {booking.booking_reference}</p>
                </div>
                
                <div class="footer">
                    <p>Best regards,<br>The DEDE TOURS TRAVEL Team</p>
                    <p>© 2024 DEDE TOURS TRAVEL. All rights reserved.</p>
                    <p>
                        <a href="tel:+254758355325">+254758355325</a> |
                        <a href="mailto:info@dedeexpeditions.com">info@dedeexpeditions.com</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(email_message, 'html'))
        s.send_message(msg)
        s.quit()
        print(f"SUCCESSFULLY SENT EMAIL to {booking.email} for booking {booking.booking_reference}")
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        raise e

def daytrip_booking(request, daytrip_slug):
    daytrip = get_object_or_404(DayTrip, slug=daytrip_slug)
    today = timezone.now().date()
    
    if request.method == 'POST':
        try:
            # Validate number of people
            try:
                number_of_people = int(request.POST.get('number_of_people', 1))
                if number_of_people < 1:
                    raise ValidationError("Number of people must be at least 1")
                
                # Check available slots
                remaining_slots = daytrip.get_remaining_slots()
                if number_of_people > remaining_slots:
                    raise ValidationError(f"Only {remaining_slots} slots available for this day trip")
            except ValueError:
                raise ValidationError("Please enter a valid number of people")

            # Calculate base price
            base_price = daytrip.price * number_of_people
            
            # Handle optional activities
            total_price = base_price
            selected_activities = []
            optional_activities = request.POST.getlist('optional_activities')
            
            if optional_activities:
                for activity_id in optional_activities:
                    try:
                        activity = OptionalActivity.objects.get(id=activity_id, daytrip=daytrip)
                        if activity.price:
                            total_price += activity.price * number_of_people
                        selected_activities.append(activity)
                    except OptionalActivity.DoesNotExist:
                        continue

            # Create new booking
            booking = DayTripBooking(
                daytrip=daytrip,
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                travel_date=daytrip.date,
                number_of_people=number_of_people,
                special_requirements=request.POST.get('special_requirements'),
                total_price=total_price,
                booking_status='pending',
                payment_status='pending'
            )
            
            # Validate the model
            booking.full_clean()
            
            # Save the booking
            booking.save()

            # Add optional activities after saving
            if selected_activities:
                booking.optional_activities.set(selected_activities)

            # Send confirmation email
            try:
                send_daytrip_confirmation_email(booking)
            except Exception as e:
                print(f"Email sending failed: {str(e)}")
                # Continue with the booking process even if email fails

            messages.success(request, 'Day Trip booking successful! Check your email for confirmation.')
            return redirect('dede:daytrip_booking_confirmation', booking_reference=booking.booking_reference)
            
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
            else:
                messages.error(request, str(e))
            print(f"Validation error: {str(e)}")  # For debugging
        except Exception as e:
            messages.error(request, 'There was an error processing your booking. Please try again.')
            print(f"Booking error: {str(e)}")  # For debugging
        
        # If there's an error, re-render the form with the submitted data
        return render(request, 'users/dede/daytrip-booking-form.html', {
            'daytrip': daytrip,
            'form_data': request.POST,
            'today': today,
        })
    
    # For GET requests, render empty form
    return render(request, 'users/dede/daytrip-booking-form.html', {
        'daytrip': daytrip,
        'today': today,
        'form_data': None,
    })

def daytrip_booking_confirmation(request, booking_reference):
    booking = get_object_or_404(DayTripBooking, booking_reference=booking_reference)
    return render(request, 'users/dede/daytrip-booking-confirmation.html', {'booking': booking})
    
class AboutView(TemplateView):
    template_name = 'users/dede/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data you want to display on the about page
        return context


def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    return render(request, 'users/dede/destination_detail.html', {'destination': destination})

# class ShopView(ListView):
#     model = Product
#     template_name = 'users/dede/shop.html'
#     context_object_name = 'products'
#     paginate_by = 9  # Number of products per page

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         # Add any filtering logic here if needed
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Add any additional context data for the shop page
#         return context

class ContactView(TemplateView):
    template_name = 'users/dede/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data for the contact page
        return context

    def post(self, request, *args, **kwargs):
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Add your contact form processing logic here
        # For example, sending an email or saving to database

        # Redirect or render response
        return render(request, self.template_name, {
            'success_message': 'Thank you for your message. We will get back to you soon!'
        })

class TourListView(ListView):
    model = Tour
    template_name = 'users/dede/tour-grid-1.html'
    context_object_name = 'tours'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destinations'] = Destination.objects.all()
        context['featured_tours'] = Tour.objects.filter(is_featured=True)
        return context

    def get_queryset(self):
        queryset = Tour.objects.all()
        destination = self.request.GET.get('destination')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        duration = self.request.GET.get('duration')
        featured = self.request.GET.get('featured')  # Add this line

        if destination:
            queryset = queryset.filter(destination__slug=destination)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if duration:
            queryset = queryset.filter(duration=duration)
        if featured:  # Add this block
            queryset = queryset.filter(is_featured=True)

        return queryset.select_related('destination')  # Optimize database queries

class TourDetailView(DetailView):
    model = Tour
    template_name = 'users/dede/tour-details.html'
    context_object_name = 'tour'
    slug_url_kwarg = 'tour_slug'  # Add this line to match the URL pattern

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = self.get_object()
        
        # Get reviews with aggregated ratings
        reviews = tour.reviews.all()
        avg_ratings = reviews.aggregate(
            avg_location=Avg('location_rating'),
            avg_price=Avg('price_rating'),
            avg_amenities=Avg('amenities_rating'),
            avg_services=Avg('services_rating'),
            avg_rooms=Avg('rooms_rating')
        )
        
        context.update({
            'reviews': reviews,
            'avg_ratings': avg_ratings,
            'highlights': tour.highlights.all(),
            'inclusions': tour.inclusions.all(),
            'tour_days': tour.tour_days.all(),
            'related_tours': Tour.objects.filter(destination=tour.destination).exclude(id=tour.id)[:3]
        })
        
        return context

def submit_review(request, tour_slug):
    if request.method == 'POST':
        tour = get_object_or_404(Tour, slug=tour_slug)
        
        review = Review(
            tour=tour,
            user_name=request.POST.get('name'),
            rating=request.POST.get('rating'),
            comment=request.POST.get('message'),
            location_rating=request.POST.get('location_rating'),
            price_rating=request.POST.get('price_rating'),
            amenities_rating=request.POST.get('amenities_rating'),
            services_rating=request.POST.get('services_rating'),
            rooms_rating=request.POST.get('rooms_rating')
        )
        review.save()
        
        # Update tour rating and review count
        tour.reviews_count = tour.reviews.count()
        tour.rating = tour.reviews.aggregate(Avg('rating'))['rating__avg']
        tour.save()
        
        messages.success(request, 'Your review has been submitted successfully!')
        # Update the redirect to use tour_slug instead of slug
        return redirect('dede:tour_detail', tour_slug=tour_slug)
    
    return redirect('dede:tour_detail', tour_slug=tour_slug)


def tour_booking(request, tour_slug):
    tour = get_object_or_404(Tour, slug=tour_slug)
    today = timezone.now().date()
    
    if request.method == 'POST':
        try:
            # Validate travel date
            travel_date = datetime.datetime.strptime(request.POST.get('travel_date'), '%Y-%m-%d').date()
            if travel_date < today:
                raise ValidationError("Travel date cannot be in the past")

            # Validate number of people
            try:
                number_of_people = int(request.POST.get('number_of_people', 1))
                if number_of_people < 1:
                    raise ValidationError("Number of people must be at least 1")
                if number_of_people > tour.group_size:
                    raise ValidationError(f"Number of people cannot exceed tour's maximum group size of {tour.group_size}")
            except ValueError:
                raise ValidationError("Please enter a valid number of people")

            # Calculate total price
            total_price = tour.price * number_of_people

            # Create new booking
            booking = Booking(
                tour=tour,
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                travel_date=travel_date,
                number_of_people=number_of_people,
                special_requirements=request.POST.get('special_requirements'),
                total_price=total_price,
                booking_status='pending',
                payment_status='pending',
                deposit_paid=0
            )
            
            # Validate the model
            booking.full_clean()
            
            # Save the booking
            booking.save()

            # Send confirmation email
            try:
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

                msg = MIMEMultipart('alternative')
                msg['From'] = "DEDE TOURS TRAVEL <novustellke@gmail.com>"
                msg['To'] = booking.email
                msg['Subject'] = f"Booking Confirmation - {booking.booking_reference}"

                email_message = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Booking Confirmation</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333333;
                            margin: 0;
                            padding: 0;
                        }}
                        .email-container {{
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                        }}
                        .header {{
                            text-align: center;
                            padding: 20px 0;
                            background-color: #f8f9fa;
                        }}
                        .logo {{
                            max-width: 200px;
                            height: auto;
                        }}
                        .content {{
                            padding: 20px 0;
                        }}
                        .booking-details {{
                            background-color: #f8f9fa;
                            padding: 20px;
                            border-radius: 5px;
                            margin: 20px 0;
                        }}
                        .footer {{
                            text-align: center;
                            padding: 20px;
                            background-color: #f8f9fa;
                            font-size: 12px;
                            color: #666;
                        }}
                        .button {{
                            display: inline-block;
                            padding: 10px 20px;
                            background-color: #4CAF50;
                            color: white;
                            text-decoration: none;
                            border-radius: 5px;
                            margin: 20px 0;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <img src="https://kipekeetravel.onrender.com/static/assets3/img/logo/dedelogo1.png" alt="DEDE TOURS TRAVEL" class="logo">
                        </div>
                        
                        <div class="content">
                            <h2>Booking Confirmation</h2>
                            <p>Dear {booking.full_name},</p>
                            
                            <p>Thank you for booking your adventure with DEDE TOURS TRAVEL! We're excited to help you explore {tour.name}.</p>
                            
                            <div class="booking-details">
                                <h3>Booking Details:</h3>
                                <p><strong>Booking Reference:</strong> {booking.booking_reference}</p>
                                <p><strong>Tour:</strong> {tour.name}</p>
                                <p><strong>Travel Date:</strong> {booking.travel_date}</p>
                                <p><strong>Number of People:</strong> {booking.number_of_people}</p>
                                <p><strong>Total Price:</strong> KES{booking.total_price}</p>
                            </div>
                            
                            <p>Your booking status is currently <strong>pending</strong>. Our team will contact you shortly regarding payment and final confirmation.</p>
                            
                            <p>If you have any questions, please contact us with your booking reference: {booking.booking_reference}</p>
                        </div>
                        
                        <div class="footer">
                            <p>Best regards,<br>The DEDE TOURS TRAVEL Team</p>
                            <p>© 2024 DEDE TOURS TRAVEL. All rights reserved.</p>
                            <p>
                                <a href="tel:++254758355325">+254758355325</a> |
                                <a href="mailto:info@dedeexpeditions.com">info@dedeexpeditions.com</a>
                            </p>
                        </div>
                    </div>
                </body>
                </html>
                """

                msg.attach(MIMEText(email_message, 'html'))
                s.send_message(msg)
                s.quit()
                print(f"SUCCESSFULLY SENT EMAIL to {booking.email} for booking {booking.booking_reference}")
            except Exception as e:
                # Log the error but don't stop the booking process
                print(f"Email sending failed: {e}")
                print(f"Error type: {type(e).__name__}")
                print(f"Error details: {str(e)}")

            messages.success(request, 'Booking successful! Check your email for confirmation.')
            return redirect('dede:booking_confirmation', booking_reference=booking.booking_reference)
            
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
            else:
                messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'There was an error processing your booking. Please try again.')
            print(f"Booking error: {str(e)}")  # For debugging
        
        # If there's an error, re-render the form with the submitted data
        return render(request, 'users/dede/booking-form.html', {
            'tour': tour,
            'form_data': request.POST,
            'today': today,
        })
    
    # For GET requests, render empty form
    return render(request, 'users/dede/booking-form.html', {
        'tour': tour,
        'today': today,
        'form_data': None,
    })

def booking_confirmation(request, booking_reference):
    booking = get_object_or_404(Booking, booking_reference=booking_reference)
    return render(request, 'users/dede/booking-confirmation.html', {'booking': booking})
