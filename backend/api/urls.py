from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test),
    path('plan-trip/', views.plan_trip),
    path('trips/', views.list_trips),
    path('trips/history/', views.get_trip_history),  # New endpoint
    path('trips/<int:trip_id>/', views.get_trip),
]

