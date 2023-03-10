from rest_framework import serializers
from .models import ProductoModel, CategoriaModel, UsuarioModel, DetallesOrdenModel, OrdenesModel

class CategoriaSerializer(serializers.ModelSerializer):
    # cuando utilizamos un serializador basandonos en un modelo se declara la clase Meta
    class Meta:
        # este se encargara de mapear todos los atributos del modelo para hacer concordar el tipo de dato y sus especificaciones
        model = CategoriaModel
        # fields > sirve para indicar que columnas de esa tabla queremos trabajar, si queremos todas las columnas entonces definiremos el valor de '__all__' caso contrario lo podremos manejar en un arreglo con los nombre de las columnas
        fields = '__all__'
        # fields = ['id', 'nombre']
        # si queremos excluir una minima cantidad de columnas para no trabajarlas entonces usaremos 
        # exclude = ['id']
        
        # NOTA: no se puede trabajar con el exclude y el fields a la vez, o es uno o es el otro

class ProductoSerializer(serializers.ModelSerializer):
    # estado = serializers.BooleanField(read_only=True)
    class Meta:
        model = ProductoModel
        # fields = ['nombre', 'precio']
        fields = '__all__'
        # exclude = ['estado']


class MostrarProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoModel
        exclude = ['disponibilidad']
        # este atributo sirve para poder conectarnos a las relaciones adyacentes a este modelo sirve solamente para tablas en las cuales tengamos una llave foranea es decir que esta tabla dependa de otra
        # sirve para decir que desde el plato nos podamos mover un nivel hacia arriba y devolver lo que vendria a ser la categoria
        depth = 1


class CrearProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoModel
        exclude = ['disponibilidad']

class CategoriaConProductosSerializer(serializers.ModelSerializer):
    # source > sirve para indicar que atributo del modelo tengo que utilizar para hacer que funcione, sin embargo si utilizamos el atributo original no es necesario colocar el source (porque dara un error de redundancia)
    info_adicional = CrearProductoSerializer(many=True, source='productos')
    class Meta:
        model = CategoriaModel
        fields = '__all__'
        
class RegistroUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = UsuarioModel
        # extra_kwargs > sirve para modificar configuracion de los atributos del modelo
        # puedo indicar el atributo y decirle que quiero que sea 'write_only' (solo escritura) 'read_only' (solo lectura)
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'nombre','apellido','correo' ]
        model = UsuarioModel
        # extra_kwargs > sirve para modificar configuracion de los atributos del modelo
        # puedo indicar el atributo y decirle que quiero que sea 'write_only' (solo escritura) 'read_only' (solo lectura)
        

class DetallesOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallesOrdenModel
        fields = ['cantidad', 'producto_id']

class OrdenesSerializer(serializers.ModelSerializer):
    usuario_id = UsuarioSerializer(source='id')
    # detalle =  DetallesOrdenSerializer(many=True, write_only=True)

    class Meta:
        model = OrdenesModel
        exclude = ['estado']

class GetOrdenesSerializer(serializers.ModelSerializer):
    # cliente = ClientesSerializer(source='id')
    # detalle
    # usuario (vendedor)
    class Meta:
        model = OrdenesModel
        fields = '__all__'