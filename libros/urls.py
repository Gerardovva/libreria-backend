from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AutorViewSet, CategoriaViewSet, EditorialViewSet, RegisterView, LoginView, UserView, LogoutView, LibroViewSet


router = DefaultRouter()
router.register(r'libros', LibroViewSet, basename='libro')
router.register(r'autores', AutorViewSet, basename='autor')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'editoriales', EditorialViewSet, basename='editorial')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
