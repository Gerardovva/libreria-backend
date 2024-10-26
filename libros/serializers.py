from rest_framework import serializers
from .models import User,Libro

class UserSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo User.

    Este serializador se encarga de la validación y creación de usuarios.
    """
    
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}  # La contraseña no se incluirá en las respuestas
        }
        
    def create(self, validated_data):
        """
        Crea un nuevo usuario utilizando los datos validados.

        Args:
            validated_data (dict): Un diccionario con los datos validados del usuario.

        Returns:
            User: La instancia del usuario creada.

        Raises:
            ValueError: Si no se proporciona una contraseña al crear el usuario.
        """
        
        password = validated_data.pop('password', None)  # Extrae la contraseña de validated_data
        user_instance = self.Meta.model(**validated_data)  # Crea una instancia del modelo User

        if password is not None:  # Si hay una contraseña
            user_instance.set_password(password)  # Establece la contraseña de manera segura
        
        user_instance.save()  # Guarda la instancia en la base de datos
        return user_instance  # Retorna la instancia del usuario creado



from rest_framework import serializers
from .models import Libro, Autor, Categoria, Editorial

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'fecha_nacimiento', 'nacionalidad']

class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = ['id', 'nombre', 'direccion', 'contacto']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class LibroSerializer(serializers.ModelSerializer):
    autor = AutorSerializer()  # Nested serializer for related author
    editorial = EditorialSerializer()  # Nested serializer for related editorial
    categorias = CategoriaSerializer(many=True)  # Nested serializer for many-to-many categories

    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'descripcion', 'imagen', 'autor', 'editorial', 'categorias', 'fecha_publicacion']
        
        
        def validate_autor(self, value):
            if not value:
                raise serializers.ValidationError("Este campo es obligatorio.")
            return value
        
        
        def validate_editorial(self, value):
            if not value:
                raise serializers.ValidationError("Este campo es obligatorio.")
            return value
                
        
        
        
        
        
