from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import Libro, User
from .serializers import LibroSerializer, UserSerializer
import jwt
import datetime
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Libro, Autor, Categoria, Editorial
from .serializers import LibroSerializer, AutorSerializer, CategoriaSerializer, EditorialSerializer


class RegisterView(APIView):
    """
    Vista para manejar el registro de nuevos usuarios.

    Métodos:
        - post: Crea un nuevo usuario en el sistema.

    Ejemplo de uso:
        Para registrar un nuevo usuario, envía una solicitud POST con los siguientes datos:
        {
            "name": "Nombre del Usuario",
            "email": "usuario@ejemplo.com",
            "password": "contraseña"
        }

    Respuesta exitosa:
        {
            "id": 1,
            "name": "Nombre del Usuario",
            "email": "usuario@ejemplo.com"
        }
    """

    def post(self, request):
        # Serializa los datos del usuario recibidos en la solicitud
        serializer = UserSerializer(data=request.data)
        # Valida los datos, lanzando una excepción si no son válidos
        serializer.is_valid(raise_exception=True)
        # Guarda el nuevo usuario en la base de datos
        serializer.save()
        # Devuelve los datos del usuario registrado
        return Response(serializer.data)
    

class LoginView(APIView):
    """
    Vista para manejar el inicio de sesión de los usuarios.

    Métodos:
        - post: Verifica las credenciales del usuario y genera un token JWT.

    Ejemplo de uso:
        Para iniciar sesión, envía una solicitud POST con los siguientes datos:
        {
            "email": "usuario@ejemplo.com",
            "password": "contraseña"
        }

    Respuesta exitosa:
        {
            "jwt": "token_jwt_generado"
        }

    Excepciones:
        - AuthenticationFailed: Se lanza si el usuario no se encuentra o si la contraseña es incorrecta.
    """

    def post(self, request):
        # Obtiene las credenciales del cuerpo de la solicitud
        email = request.data.get('email')
        password = request.data.get('password')

        # Verifica si el usuario existe
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('Usuario no encontrado')  # Lanza la excepción

        # Confirma que la contraseña es correcta
        if not user.check_password(password):
            raise AuthenticationFailed('Contraseña incorrecta')  # Lanza la excepción
        
        # Crea el payload para el token JWT
        payload = {
            'id': user.id,  # ID del usuario
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60),  # Tiempo de expiración
            'iat': datetime.datetime.now(datetime.timezone.utc),  # Tiempo de emisión
        }
        
        # Genera el token JWT utilizando la clave secreta
        token = jwt.encode(payload, 'secret', algorithm='HS256')  # Cambia 'secret' por una clave más segura

        # Respuesta de éxito si las credenciales son correctas
        response = Response()
        # Establece una cookie para el token JWT (opcional)
        response.set_cookie(key='jwt', value=token, httponly=True)

        # Devuelve la respuesta con el token JWT
        response.data = {
            'jwt': token
        }        
        return response




class UserView(APIView):
    def get(self, request):
        # Obtiene el token JWT de la cookie
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Token JWT no válido')  # Lanza la excepción
        
        try:
            # Decodifica el token JWT utilizando la clave secreta
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token JWT expirado')  # Lanza la excepción
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token JWT no válido')  # Lanza la excepción
        
        # Obtiene el usuario correspondiente al ID del payload
        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)  # Serializa los datos del usuario
        return Response(serializer.data)
    
    
    

class LogoutView(APIView):
    def post(self, request):
        response=Response()
        response.delete_cookie('jwt')  # Elimina la cookie JWT
        response.data = {'mensaje': 'Sesión finalizada'}
        
        return response
    
    



# ViewSet para libros
class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    # permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    # Filtro personalizado para obtener libros por autor
    @action(detail=False, methods=['get'], url_path='por-autor/(?P<autor_id>[^/.]+)')
    def por_autor(self, request, autor_id=None):
        libros = Libro.objects.filter(autor__id=autor_id)
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)

    # Filtro personalizado para obtener libros por categoría
    @action(detail=False, methods=['get'], url_path='por-categoria/(?P<categoria_id>[^/.]+)')
    def por_categoria(self, request, categoria_id=None):
        libros = Libro.objects.filter(categorias__id=categoria_id)
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)

    # Filtro personalizado para obtener libros por editorial
    @action(detail=False, methods=['get'], url_path='por-editorial/(?P<editorial_id>[^/.]+)')
    def por_editorial(self, request, editorial_id=None):
        libros = Libro.objects.filter(editorial__id=editorial_id)
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)

# ViewSet para autores
class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

# ViewSet para categorías
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# ViewSet para editoriales
class EditorialViewSet(viewsets.ModelViewSet):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializer
