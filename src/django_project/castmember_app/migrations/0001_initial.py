# Generated by Django 5.1.4 on 2025-01-14 18:43

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CastMember',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('ACTOR', 'ACTOR'), ('DIRECTOR', 'DIRECTOR')], max_length=8)),
            ],
            options={
                'db_table': 'cast_members',
            },
        ),
    ]
