from rest_framework import viewsets
from .models import Cliente, Pago
from .serializers import ClienteSerializer, PagoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
	queryset = Cliente.objects.all().order_by('nombre_propietario')
	serializer_class = ClienteSerializer

class PagoViewSet(viewsets.ModelViewSet):
	queryset = Pago.objects.all().order_by('cliente','fecha')
	serializer_class = PagoSerializer