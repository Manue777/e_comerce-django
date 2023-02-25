# Generated by Django 4.1.5 on 2023-02-25 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_usuariomodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenesModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=45)),
                ('observacion', models.CharField(max_length=100, null=True)),
                ('estado', models.BooleanField(default=True, null=True)),
                ('usuario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ordenes',
            },
        ),
        migrations.CreateModel(
            name='DetallesOrdenModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('orden_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.ordenesmodel')),
                ('producto_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.productomodel')),
            ],
            options={
                'db_table': 'detalles_orden',
            },
        ),
    ]