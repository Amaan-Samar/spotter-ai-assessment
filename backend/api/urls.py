from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('plan-trip/', views.plan_trip, name='plan-trip'),
    path('trips/', views.list_trips, name='list-trips'),
    path('trips/<int:trip_id>/', views.get_trip, name='get-trip'),
]
