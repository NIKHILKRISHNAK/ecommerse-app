# Generated by Django 4.2.1 on 2023-06-25 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='image',
            field=models.ImageField(upload_to='uploads/'),
        ),
    ]
