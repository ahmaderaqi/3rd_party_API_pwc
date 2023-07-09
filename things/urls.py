from django.urls import path
from .views import event_list_view,flights_view,weather_view
urlpatterns = [
     path('/flights/', flights_view, name='flights'),
    path('/weather/', weather_view, name='weather'),
    path('/events/', event_list_view, name='event-list'),

]