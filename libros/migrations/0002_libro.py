# Generated by Django 5.1.2 on 2024-10-26 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=100, verbose_name='Título')),
                ('imagen', models.ImageField(null=True, upload_to='imagenes/', verbose_name='Imagen')),
                ('descripcion', models.TextField(null=True, verbose_name='Descripcion')),
            ],
        ),
    ]