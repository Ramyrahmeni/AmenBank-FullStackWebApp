from django.db import models

# Create your models here.
class utilisateur(models.Model):
  nom = models.CharField(max_length=255)
  prenom = models.CharField(max_length=255)
  adresse=models.CharField(max_length=1000)
  adresse_email=models.EmailField(unique=True)
  preference_linguistique=models.CharField(max_length=255)
  compte_par_defaut = models.CharField(max_length=1000, null=True, blank=True)
  nombre_connexions=models.IntegerField(default=0)
  mailbox=models.CharField(default='E-mail',max_length=200)
  mot_de_passe=models.CharField(max_length=1000)
  login = models.CharField(max_length=255, unique=True, primary_key=True)

  class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

  def __str__(self):
        return f"{self.login}"

class Compte(models.Model):
    num_compte = models.CharField(max_length=255,primary_key=True, unique=True)
    libelle = models.CharField(max_length=200, unique=True)
    date_solde = models.DateField()
    solde = models.IntegerField()
    alerte_mail = models.CharField(max_length=200)
    alerte_sms = models.CharField(max_length=200)
    login = models.ForeignKey(utilisateur, on_delete=models.CASCADE, to_field='login')

    def __str__(self):
        return self.libelle
 