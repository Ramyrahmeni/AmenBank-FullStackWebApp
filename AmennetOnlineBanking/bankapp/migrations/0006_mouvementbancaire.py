# Generated by Django 4.2.3 on 2023-07-18 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0005_rename_preference_lingustique_utilisateur_preference_linguistique_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MouvementBancaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('debit', 'Débit'), ('credit', 'Crédit')], max_length=10)),
                ('compte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankapp.compte')),
            ],
        ),
    ]
