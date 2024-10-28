# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255, unique=True)
#     password = models.CharField(max_length=255)
#     username = None
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
    
# class Libro(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     titulo = models.CharField(max_length=100, verbose_name='Título')
#     imagen = models.ImageField(upload_to='imagenes/', verbose_name='Imagen', null=True)
#     descripcion = models.TextField(verbose_name='Descripcion', null=True)

#     def __str__(self):
#         return f'Titulo: {self.titulo} - Descripcion: {self.descripcion}'
    
#     def delete(self, using=None, keep_parents=False):
#         self.imagen.storage.delete(self.imagen.name)
#         super().delete()




from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre = models.CharField(max_length=100)   
    fecha_nacimiento = models.DateField(null=True, blank=True)
    nacionalidad = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Editorial(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.EmailField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=100, verbose_name='Título')
    imagen = models.ImageField(upload_to='imagenes/', verbose_name='Imagen', null=True)
    descripcion = models.TextField(verbose_name='Descripcion', null=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="libros")
    editorial = models.ForeignKey(Editorial, on_delete=models.SET_NULL, null=True, blank=True)  # Corrected field name
    categorias = models.ManyToManyField(Categoria, related_name="libros")
    fecha_publicacion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Titulo: {self.titulo} - Descripcion: {self.descripcion}'

    def delete(self, using=None, keep_parents=False):
        if self.imagen:
            self.imagen.storage.delete(self.imagen.name)
        super().delete()