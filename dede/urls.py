from django.urls import path
from . import views

app_name = 'dede'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('tours/', views.TourListView.as_view(), name='tour_list'),
    path('tour/<slug:slug>/', views.TourDetailView.as_view(), name='tour_detail'),
    path('tour/<slug:tour_slug>/review/', views.submit_review, name='submit_review'),
]