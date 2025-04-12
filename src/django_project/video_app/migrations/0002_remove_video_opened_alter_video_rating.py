# Generated by Django 5.2 on 2025-04-12 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='opened',
        ),
        migrations.AlterField(
            model_name='video',
            name='rating',
            field=models.CharField(choices=[('ER', 'ER'), ('L', 'L'), ('AGE_10', 'AGE_10'), ('AGE_12', 'AGE_12'), ('AGE_14', 'AGE_14'), ('AGE_16', 'AGE_16'), ('AGE_18', 'AGE_18')], max_length=10),
        ),
    ]
