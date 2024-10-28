from rest_framework import serializers
from .models import Autor, Categoria, Editorial, User,Libro
from .models import Libro, Autor, Editorial, Categoria

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
    autor = serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all())
    editorial = serializers.PrimaryKeyRelatedField(queryset=Editorial.objects.all())
    categorias = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), many=True)

    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'descripcion', 'imagen', 'autor', 'editorial', 'categorias', 'fecha_publicacion']

    def validate_autor(self, value):
        if value is None:
            raise serializers.ValidationError("El autor es obligatorio.")
        return value

    def validate_editorial(self, value):
        if value is None:
            raise serializers.ValidationError("La editorial es obligatoria.")
        return value

    def create(self, validated_data):
        # If categorias is included in the validated data, pop it
        categorias = validated_data.pop('categorias', None)
        libro = Libro.objects.create(**validated_data)
        if categorias:
            libro.categorias.set(categorias)  # Set many-to-many relationships
        return libro

    def update(self, instance, validated_data):
        categorias = validated_data.pop('categorias', None)
        instance.titulo = validated_data.get('titulo', instance.titulo)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.imagen = validated_data.get('imagen', instance.imagen)
        instance.autor = validated_data.get('autor', instance.autor)
        instance.editorial = validated_data.get('editorial', instance.editorial)
        instance.fecha_publicacion = validated_data.get('fecha_publicacion', instance.fecha_publicacion)
        instance.save()
        if categorias is not None:
            instance.categorias.set(categorias)  # Update many-to-many relationships
        return instance
   
        
