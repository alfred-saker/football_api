# Generated by Django 4.2 on 2023-09-04 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='flag_url',
            new_name='flag_urls',
        ),
    ]
