# Generated by Django 5.1.2 on 2024-10-28 13:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0002_remove_libro_editorial_libro_ditorial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libro',
            name='ditorial',
        ),
        migrations.AddField(
            model_name='libro',
            name='editorial',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='libros.editorial'),
        ),
    ]
