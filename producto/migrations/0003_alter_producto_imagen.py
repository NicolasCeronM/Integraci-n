# Generated by Django 5.0.5 on 2024-05-17 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0002_alter_producto_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(default='media/producto/default.jpg', null=True, upload_to='producto'),
        ),
    ]
