from django.conf.urls import url, include
from rest_framework import routers

from .views import ClienteViewSet, PagoViewSet

router = routers.SimpleRouter()
router.register(r'cliente',ClienteViewSet)
router.register(r'pago',PagoViewSet)

urlpatterns = [
  url(r'^', include(router.urls)),
]