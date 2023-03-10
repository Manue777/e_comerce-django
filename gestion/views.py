from rest_framework.generics import ListCreateAPIView, DestroyAPIView, ListAPIView,CreateAPIView, UpdateAPIView
from .models import CategoriaModel, ProductoModel, UsuarioModel,OrdenesModel,DetallesOrdenModel
from .serializers import CategoriaSerializer, ProductoSerializer, CrearProductoSerializer, CategoriaConProductosSerializer, MostrarProductoSerializer, RegistroUsuarioSerializer, OrdenesSerializer, DetallesOrdenSerializer, GetOrdenesSerializer

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from .permissions import SoloAdministradores, SoloTrabajador

from rest_framework import  status
# List > Listar (get)
# Create > Crear (post)

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import transaction



class CategoriaApiView(ListCreateAPIView):
    # secuencia de permisos > el primer permiso se debe de cumplir para continuar con el segundo permiso y asi sucesivamente, si alguno falla (retorna False) entonces todo termina
    permission_classes = [IsAuthenticated, SoloAdministradores]
    # al utilizar una vista generica que ya no es necesario definir el comportamiento para cuando sea get o post
    # queryset > el comando que utilizara para llamar a la informacion de nuestra base de datos
    # SELECT * FROM categoria;
    queryset = CategoriaModel.objects.all()
    # serializer_class > se define una clase que se encargara de convertir y transformar la informacion que viene desde el cliente y la informacion que enviamos hacia el cliente en dato legibles

    serializer_class = CategoriaSerializer
    # ya no es necesario definir los metodos 'get' y 'post'
    # def get(self):
    #     pass

    # def post(self):
    #     pass

class ProductoApiView(ListCreateAPIView):
    queryset = ProductoModel.objects.all()
    # serializer_class > cuando nosotros modificamos la funcionabilidad de los metodos ya no es necesario definir los atributos obligatorios (y queryset)

    def get(self, request: Request):
        # al colocar ':' indicamos que el tipo de dato que sera esa variable en el caso que no la hemos seteado correctamente
        # request > toda la informacion que viene del cliente
        
        # SELECT * FROM platos WHERE disponibilidad = true;
        resultado = ProductoModel.objects.filter(disponibilidad=True).all()
        print(resultado)
        # aca llamamos al serializer y le pasamos la informacion proveniente de la bd y con el parametro many True indicamos que le estamos pasando un arreglo de instancias
        serializador = MostrarProductoSerializer(instance=resultado, many=True)
        print(serializador.data)

        return Response(data= {
            'content': serializador.data
        })
    

    def post(self, request:Request):
        body = request.data
        # cuando queremos verificar si la informacion entrante es valida entonces utilizamos el parametro data en vez del parametro instance
        serializador = CrearProductoSerializer(data=body)

        # es el encargado de validar si la data es correcta y cumple con todos los requisitos
        valida = serializador.is_valid()

        # SELECT * FROM platos WHERE nombre = '...' LIMIT 1;
        productoExistente = ProductoModel.objects.filter(nombre = body.get('nombre')).first()

        if productoExistente : 
            return Response(data={
                'message': 'El productos con nombre {} ya existe'.format(productoExistente.nombre)
            })

        if valida == False:
            return Response(data={
                'message': 'La informacion es invalida',
                # error > mostrar los errores SOLAMENTE cuando la data no sea valida
                'content': serializador.errors

            })


        # si la data pasada al serializador es una data valida entonces esta informacion se guardara en el atributo validated_data que es un diccionario, el validated_data solamente estara disponible cuando mandemos a la validacion, si no se hace la validacion el validated_data sera vacio
        # platoExistente = PlatoModel.objects.filter(nombre = serializador.validated_data.get('nombre')).first()

        # if platoExistente : 
        #     return Response(data={
        #         'message': 'El plato con nombre {} ya existe'.format(platoExistente.nombre)
        #     })
        
        print(serializador.validated_data)
        # asi guardamos la informacion en la base de datos utilizando el serializador
        nuevoProducto = serializador.save()
        print(nuevoProducto)

        serializar = MostrarProductoSerializer(instance=nuevoProducto)
        return Response(data={
            'message': 'Producto creado exitosamente',
            # data > es la informacion convertida a un diccionario para que pueda ser entendida por el cliente
            'content': serializar.data
        })


class ProductoDestroyApiView(DestroyAPIView):
    # queryset = PlatoModel.objects.all()
    # serializer_class = PlatoSerializer
    permission_classes = [IsAuthenticated, SoloTrabajador]
    def delete(self, request: Request, pk: int):
        print(pk)
        productoEncontrado = ProductoModel.objects.filter(id = pk, disponibilidad = True).first()

        if productoEncontrado is None:
            return Response(data={
                'message': 'El producto no existe'
            })
        
        # Le cambiamos la disponibilidad
        productoEncontrado.disponibilidad = False
        
        # guardamos los cambios en la bd
        productoEncontrado.save()

        return Response(data={
            'message': 'Producto eliminado exitosamente'
        })

class ListarCategoriaApiView(ListAPIView):
    def get(self, request:Request, pk : int):
        # SELECT * FROM CATEGORIAS WHERE ID = ... LIMIT 1;
        categoriaEncontrada = CategoriaModel.objects.filter(id= pk).first()
        print(categoriaEncontrada)

        if categoriaEncontrada is None:
            return Response(data={
                'message': 'Categoria no existe'
            })
        # dir(instancia) > nos muestra todos los atributos y metodos de la clase
        # print(dir(categoriaEncontrada))
        
        # SELECT * FROM platos WHERE categoria_id = ... AND id = 10;
        print(categoriaEncontrada.productos.filter(id=10).all())
        producto = categoriaEncontrada.productos.all()[0] # estamos accediendo al primer plato de esta categoria
        print(producto.nombre)
        print(producto.id)
        print(producto.precio)
        print(producto.fechaCreacion)

        serializador = CategoriaConProductosSerializer(instance=categoriaEncontrada)


        return Response(data={
            'content': serializador.data
        })

class RegistroUsuarioApiView(CreateAPIView):
    def post(self, request: Request):
        serializador = RegistroUsuarioSerializer(data = request.data)
        validacion = serializador.is_valid()

        if validacion is False:
            return Response(data={
                'message': 'error al crear el usuario',
                'content': serializador.errors
            }, status=400)
        
        # inicializo el nuevo usuario con la informacion validada
        nuevoUsuario = UsuarioModel(**serializador.validated_data)
        # ahora genero el hash de la contrase??a
        nuevoUsuario.set_password(serializador.validated_data.get('password'))
        # guardo el usuario en la base de datos
        nuevoUsuario.save()

        return Response(data={
            'message': 'Usuario creado exitosamente'
        }, status=201)


class ActualizarCategoriaApiView(UpdateAPIView):
    queryset = CategoriaModel.objects.all()
    serializer_class = CategoriaSerializer

    def put(self, request, categoria_id):
        try:
            categoria = self.get_queryset().get(id=categoria_id)
            serializer = self.get_serializer(categoria, data=request.data)
            if serializer.is_valid():
                categoria_actualizada = serializer.update(categoria, serializer.validated_data)
                nuevo_serializador = self.get_serializer(categoria_actualizada)
                return Response(nuevo_serializador.data, status=status.HTTP_201_CREATED)

            # error = 'Faltan campos'
            # for campo in categoria.errors:
            #     error = error + ' ' + campo + ', '
            return Response({
                'message': 'faltan campos'
            })
        except Exception as e:
            return Response({
                'message': 'Internal server error',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActualizarProductoApiView(UpdateAPIView):
    queryset = ProductoModel.objects.all()
    serializer_class = ProductoSerializer

    def put(self, request, producto_id):
        try:
            producto = self.get_queryset().get(id=producto_id)
            serializer = self.get_serializer(producto, data=request.data)
            if serializer.is_valid():
                producto_actualizado = serializer.update(producto, serializer.validated_data)
                nuevo_serializador = self.get_serializer(producto_actualizado)
                return Response(nuevo_serializador.data, status=status.HTTP_201_CREATED)

            # error = 'Faltan campos'
            # for campo in categoria.errors:
            #     error = error + ' ' + campo + ', '
            return Response({
                'message': 'faltan campos'
            })
        except Exception as e:
            return Response({
                'message': 'Internal server error',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class OrdenesView(generics.GenericAPIView):
    queryset = OrdenesModel.objects.all()
    serializer_class = OrdenesSerializer

    # @transaction.atomic
    def post(self, request):
        try:
            print (request.data)
            orden = self.get_serializer(data=request.data)
            if orden.is_valid():
                usuario = UsuarioModel(**request.data['usuario'])
                usuario.save()

                # usuario = User.objects.get(id=request.data['usuario_id'])
                orden_dict = {
                    'codigo': request.data['codigo'],
                    'observacion': request.data['observacion'],
                    # 'usuario_id': usuario
                }
                orden = OrdenesModel(**orden_dict)
                orden.save()

                for detalle in request.data['detalle']:
                    producto = ProductoModel.objects.get(id=detalle['producto_id'])
                    detalle_dict = {
                        'cantidad': detalle['cantidad'],
                        'producto_id': producto,
                        'orden_id': orden
                    }
                    detalle = DetallesOrdenModel(**detalle_dict)
                    detalle.save()
            return Response({
                    'message': 'Operacion exitosa'
            }, status=status.HTTP_201_CREATED)
            error = 'Faltan campos'
            for campo in orden.errors:
                error = error + ' ' + campo + ', '
            return Response({
                'message': error
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': 'Internal server error',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  