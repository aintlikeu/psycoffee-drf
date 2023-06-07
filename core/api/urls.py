from django.urls import path, include
from api.views.spots import SimpleSpotView
# from api.routers import router


urlpatterns = [
    path('spots/', SimpleSpotView.as_view())
    # path('', include(router.urls)),
]
