from rest_framework import routers
from api.views.spots import SimpleSpotViewSet

router = routers.DefaultRouter()
router.register(r'spots', SimpleSpotViewSet, basename='spots')
