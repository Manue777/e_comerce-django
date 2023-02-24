# Generated by Django 4.1.5 on 2023-02-24 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('estado', models.BooleanField(default=True, null=True)),
            ],
            options={
                'db_table': 'categorias',
                'ordering': ['nombre', 'id'],
            },
        ),
        migrations.CreateModel(
            name='ProductoModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.CharField(max_length=80, unique=True)),
                ('precio', models.FloatField()),
                ('disponibilidad', models.BooleanField(default=True)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')),
                ('estado', models.BooleanField(default=True, null=True)),
                ('categoria', models.ForeignKey(db_column='categoria_id', on_delete=django.db.models.deletion.PROTECT, related_name='productos', to='gestion.categoriamodel')),
            ],
            options={
                'db_table': 'productos',
            },
        ),
    ]