# Generated by Django 5.1.4 on 2025-01-02 17:13

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'category',
            },
        ),
    ]
