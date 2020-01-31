from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

from django.db.models.signals import post_init, pre_delete
from django.dispatch import receiver


class Cliente(models.Model):

	# Propiedades para medir el consumo del cliente y el estado de solvencia
	cant_agua_inicio_mes = models.PositiveIntegerField()
	cant_agua_final_mes = models.PositiveIntegerField(null=True)
	fecha_ultima_actualizacion = models.DateTimeField(default=timezone.now)
	saldo_acumulado = models.IntegerField(default = 0)


	# Propiedades personales del cliente
	nombre_propietario = models.CharField(max_length=80)
	telf_propietario_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
							message="Teléfono debe tener el formato: '+999999999'. Sólo se permite hasta 15 dígitos.")
	telf_propietario = models.CharField(validators=[telf_propietario_regex], max_length=17)
	direccion = models.TextField()

	def __str__(self):
		return "ID: "+str(self.id) + " Nombre:" + self.nombre_propietario + " Telf:"+self.telf_propietario + " Saldo Acumulada:$"+str(self.saldo_acumulado)

	def set_cant_agua_inicio (self,value):
		self.cant_agua_inicio_mes = value
		if self.fecha_ultima_actualizacion <= timezone.now():
			self.fecha_ultima_actualizacion = timezone.now()
			self.save()
		else:
			raise ValidationError("CLIENT DB ERROR: No se puede setear esta propiedad porque la fecha de la última actualización es más reciente que la fecha de edición")

	def set_cant_agua_final (self,value):
		if self.fecha_ultima_actualizacion <= timezone.now():
			self.cant_agua_final_mes = value
			self.fecha_ultima_actualizacion = timezone.now()
			self.save()
		else:
			raise ValidationError("CLIENT DB ERROR: No se puede setear esta propiedad porque la fecha de la última actualización es más reciente que la fecha de edición")



class Pago(models.Model):
	cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False, blank=False)
	fecha = models.DateTimeField(default=timezone.now)
	num_confirmacion = models.PositiveIntegerField()
	monto = models.PositiveIntegerField()


# Para actualizar saldo cada vez que se registra un pago
@receiver(post_init, sender=Pago)
def update_saldo_on_create(sender , instance , **kwargs):
	instance.cliente.saldo_acumulado += instance.monto
	instance.cliente.save()

# Para actualizar saldo cada vez que se elimine un pago
@receiver(pre_delete, sender=Pago, dispatch_uid='pago_delete_signal')
def update_saldo_on_delete(sender , instance , using, **kwargs):
	instance.cliente.saldo_acumulado -= instance.monto
	instance.cliente.save()