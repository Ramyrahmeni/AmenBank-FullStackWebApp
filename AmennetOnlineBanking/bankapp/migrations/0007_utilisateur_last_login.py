# Generated by Django 4.2.3 on 2023-07-19 10:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0006_mouvementbancaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
