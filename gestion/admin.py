from django.contrib import admin
from .models import ProductoModel, CategoriaModel, UsuarioModel

# Register your models here.

class ShowFields(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'estado', 'descripcion', 'categoria')

admin.site.register(ProductoModel, ShowFields)



class ShowFields(admin.ModelAdmin):
    list_display = ('nombre', 'estado')

admin.site.register(CategoriaModel, ShowFields)




class ShowFields(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'correo')

admin.site.register(UsuarioModel, ShowFields)