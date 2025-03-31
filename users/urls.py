from django.urls import path,include
from . import views 

app_name = 'users'

urlpatterns = [
    path('', views.home, name='users-home'),
    path('about/', views.aboutus, name='aboutus'),
    path('corporate/', views.corporate, name='corporatepage'),
    path('holidays/', views.holidays, name='holidayspage'),
    path('mice/', views.micepage, name='micepage'),
    path('contactus/', views.contactus, name='contactus'),
    path('register/',views.register,name='users-register'),
    path('success/', views.success, name='success'),
    path('destination/<int:id>/',views.destination,name='users-destination'),
    path('search/',views.search, name="search"),
    path('packages/', views.all_packages, name='all_packages'),
    path('package/<int:package_id>/', views.detail_package, name='users-detail-package'),
    path('bookings/<int:package_id>/', views.bookings, name='users-bookings'),
    path('booking_success/<int:booking_id>/', views.booking_success, name='users-booking-success'),
    path('activate/<uid64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('send-mice-email/', views.send_mice_email, name='send_mice_email'),
] 
