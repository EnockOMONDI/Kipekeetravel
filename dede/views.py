from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.db.models import Avg
from .models import Destination, Tour, Review
from django.views.generic.edit import CreateView
from .models import Tour, Booking
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




class HomeView(ListView):
    model = Tour
    template_name = 'users/dede/index.html'
    context_object_name = 'tours'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_tours'] = Tour.objects.filter(rating__gte=4.5)[:6]
        context['popular_destinations'] = Destination.objects.all()[:6]
        return context
    
class AboutView(TemplateView):
    template_name = 'users/dede/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data you want to display on the about page
        return context

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
        return context

    def get_queryset(self):
        queryset = Tour.objects.all()
        destination = self.request.GET.get('destination')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        duration = self.request.GET.get('duration')

        if destination:
            queryset = queryset.filter(destination__slug=destination)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if duration:
            queryset = queryset.filter(duration=duration)

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
                                <a href="tel:+254123456789">+254 123 456 789</a> |
                                <a href="mailto:info@dedetours.com">info@dedetours.com</a>
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
