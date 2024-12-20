# Generated by Django 5.1.2 on 2024-11-01 07:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='pgRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField(max_length=500)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('room', models.TextField(max_length=50)),
                ('price', models.IntegerField()),
                ('food', models.TextField(max_length=50)),
                ('complaint', models.TextField(max_length=5000)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
