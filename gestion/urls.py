from django.urls import path
from .views import CategoriaApiView, ProductoApiView, ProductoDestroyApiView, ListarCategoriaApiView, RegistroUsuarioApiView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    # cuando se acceda a la ruta /categorias/ se mandara a llamar a la funcionabilidad de nuestro CategoriaApiView
    path('categorias/', CategoriaApiView.as_view()),
    path('productos/', ProductoApiView.as_view()),
    path('producto/<int:pk>', ProductoDestroyApiView.as_view()),
    path('categoria/<int:pk>', ListarCategoriaApiView.as_view()),
    path('registro/', RegistroUsuarioApiView.as_view()),
    path('login/', TokenObtainPairView.as_view())
]