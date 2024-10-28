# Generated by Django 5.1.2 on 2024-10-28 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0003_remove_libro_ditorial_libro_editorial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libro',
            name='editorial',
        ),
        migrations.AddField(
            model_name='libro',
            name='ditorial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='libros.editorial'),
        ),
    ]
