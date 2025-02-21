# Generated by Django 2.2.3 on 2020-01-31 20:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant_agua_inicio_mes', models.PositiveIntegerField()),
                ('cant_agua_final_mes', models.PositiveIntegerField(null=True)),
                ('fecha_ultima_actualizacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('saldo_acumulado', models.IntegerField(default=0)),
                ('nombre_propietario', models.CharField(max_length=80)),
                ('telf_propietario', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Teléfono debe tener el formato: '+999999999'. Sólo se permite hasta 15 dígitos.", regex='^\\+?1?\\d{9,15}$')])),
                ('direccion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('num_confirmacion', models.PositiveIntegerField()),
                ('monto', models.PositiveIntegerField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreapp.Cliente')),
            ],
        ),
    ]
