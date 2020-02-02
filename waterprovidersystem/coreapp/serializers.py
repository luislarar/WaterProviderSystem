from .models import Cliente, Pago
from rest_framework import serializers
from django.utils import timezone

base_cost=100
mult_cost = 1250

class ClienteSerializer (serializers.HyperlinkedModelSerializer):

	def create (self,validated_data):
		cant_agua_final_mes = validated_data.pop('cant_agua_final_mes')

		cliente = Cliente.objects.create(**validated_data)
		if cant_agua_final_mes:
			cant_agua_inicio_mes = validated_data.pop('cant_agua_inicio_mes')
			if cant_agua_final_mes > cant_agua_inicio_mes:
				raise serializers.ValidationError({'error':'La cantidad de agua al final del mes debe ser menor o igual a la inicial.'})
			cliente.cant_agua_final_mes = cant_agua_final_mes
			if cant_agua_final_mes == cant_agua_inicio_mes:
				cliente.saldo_acumulado -= base_cost
			else:
				cliente.saldo_acumulado -= (cant_agua_inicio_mes - cant_agua_final_mes)*mult_cost
			cliente.save()
		return cliente

	def update (self, instance, validated_data):
		cant_agua_final_mes = validated_data.pop('cant_agua_final_mes')
		cant_agua_inicio_mes = validated_data.pop('cant_agua_inicio_mes')

		if cant_agua_inicio_mes != instance.cant_agua_inicio_mes:
			if instance.cant_agua_final_mes and instance.cant_agua_final_mes > cant_agua_inicio_mes:
				if not cant_agua_final_mes or (cant_agua_final_mes and cant_agua_final_mes > cant_agua_inicio_mes):
					raise serializers.ValidationError({'error':'La medición al final del período debe ser mayor a la inicial. Por favor corrija los errores del formulario.'})
				else:
					instance.cant_agua_final_mes  = cant_agua_final_mes
			instance.cant_agua_inicio_mes = cant_agua_inicio_mes

		if cant_agua_final_mes:
			if cant_agua_final_mes < cant_agua_inicio_mes:
				consumed_cost = (cant_agua_inicio_mes - cant_agua_final_mes)*mult_cost
				instance.saldo_acumulado -= consumed_cost
				instance.fecha_ultima_actualizacion = timezone.now()
				return super().update(instance,validated_data)
			elif cant_agua_final_mes == cant_agua_inicio_mes:
				instance.saldo_acumulado -= base_cost
				instance.fecha_ultima_actualizacion = timezone.now()
				return super().update(instance,validated_data)
			else:
				raise serializers.ValidationError({'error':'La cantidad de agua al final del mes debe ser menor o igual a la inicial.'})
		else:
			instance.fecha_ultima_actualizacion = timezone.now()
			return super().update(instance,validated_data)



	class Meta:
		model = Cliente
		fields = ('id','cant_agua_inicio_mes','cant_agua_final_mes','saldo_acumulado','consumo_mes',
					'nombre_propietario','telf_propietario',
					'direccion')
		read_only_fields = ('saldo_acumulado','consumo_mes')

class PagoSerializer (serializers.HyperlinkedModelSerializer):

	def create(self, validated_data):
		monto = validated_data.pop('monto')
		if monto == 0:
			raise serializers.ValidationError({'error':'El monto de un pago debe ser mayor a cero.'})
		validated_data['monto']=monto
		return Pago.objects.create(**validated_data)

	class Meta:
		model = Pago
		fields = ('id','cliente','fecha','num_confirmacion','monto')