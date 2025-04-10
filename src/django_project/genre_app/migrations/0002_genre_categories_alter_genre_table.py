# Generated by Django 5.1.4 on 2025-01-06 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_app', '0001_initial'),
        ('genre_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='categories',
            field=models.ManyToManyField(related_name='genres', to='category_app.category'),
        ),
        migrations.AlterModelTable(
            name='genre',
            table='genres',
        ),
    ]
