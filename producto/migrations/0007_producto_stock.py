# Generated by Django 5.0.5 on 2024-05-17 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0006_alter_producto_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='stock',
            field=models.IntegerField(null=True),
        ),
    ]
