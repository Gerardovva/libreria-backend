# Generated by Django 5.1.2 on 2024-10-28 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0004_remove_libro_editorial_libro_ditorial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='libro',
            old_name='ditorial',
            new_name='editorial',
        ),
    ]
