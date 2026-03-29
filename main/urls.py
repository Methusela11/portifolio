from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('messages/', views.contact_messages, name='contact_messages')]
