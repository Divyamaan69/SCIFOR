# Generated by Django 5.1.2 on 2024-11-02 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pg', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pgroom',
            old_name='guest',
            new_name='user',
        ),
    ]
