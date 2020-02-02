from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Cliente, Pago
from .serializers import ClienteSerializer, PagoSerializer

class Error500View(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = '500.html'

class Error404View(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = '404.html'

class Index(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'index.html'

	def get(self,request):
		return Response({})

class ClienteList(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'clientes.html'

	def get(self, request):
		queryset = Cliente.objects.all()
		return Response({'listgiven': queryset})

class ClienteCreate(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'cliente_edit.html'

	def get(self, request):
		serializer = ClienteSerializer()
		return Response({'serializer': serializer, 'edition_mode': False})

	def post(self, request):
		serializer = ClienteSerializer(data=request.data)
		if not serializer.is_valid():
			return Response({'serializer': serializer, 'edition_mode': False})
		serializer.save()
		return redirect('clientes')


class ClienteEdit(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'cliente_edit.html'

	def get(self, request, pk):
		cliente = get_object_or_404(Cliente, id=pk)
		serializer = ClienteSerializer(cliente)
		return Response({'serializer': serializer, 'cliente':cliente,'edition_mode': True})

	def post(self, request, pk):
		cliente = get_object_or_404(Cliente, id=pk)
		serializer = ClienteSerializer(cliente, data=request.data)
		if not serializer.is_valid():
			return Response({'serializer': serializer, 'cliente':cliente,'edition_mode': True})
		serializer.save()
		return redirect('clientes')

class PagoList(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'pagos.html'

	def get(self, request):
		queryset = Pago.objects.all()
		return Response({'listgiven': queryset})