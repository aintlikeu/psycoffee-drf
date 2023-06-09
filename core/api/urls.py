from django.urls import path
from api.views.spots import SimpleSpotView, FreeSpotView
from api.views.bookings import BookingView


urlpatterns = [
    path('spots/', SimpleSpotView.as_view()),
    path('bookings/', BookingView.as_view()),
    path('free_spots/', FreeSpotView.as_view()),
]
