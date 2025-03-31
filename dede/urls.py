from django.urls import path
from . import views

app_name = 'dede'

urlpatterns = [
    path('', views.index, name='index'),
]

