from django.db import models
from django.utils import timezone
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
  last_login = models.DateTimeField(default=timezone.now)

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
        return self.num_compte
class MouvementBancaire(models.Model):
    TYPE_CHOICES = (
        ('debit', 'Débit'),
        ('credit', 'Crédit'),
    )

    compte = models.ForeignKey(Compte, on_delete=models.CASCADE)
    date = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"Mouvement #{self.pk} - Compte: {self.compte}, Montant: {self.montant}, Type: {self.get_type_display()}"
class Virement(models.Model):
    DEBIT = 'debit'
    CREDIT = 'credit'
    AVEC_BENEFICIAIRE = 'avec_beneficiaire'


    compte_a_debiter = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='virements_a_debiter')
    compte_a_crediter = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='virements_a_crediter')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    motif_payment = models.TextField()
    date_execution = models.DateField()

    beneficiaire = models.CharField(max_length=255, default='aucun')
    nom_raison_sociale = models.CharField(max_length=255, default='aucun')
    banque = models.CharField(max_length=255, default='aucun')

    def __str__(self):
        return f"Virement #{self.pk} , Montant: {self.montant}, Compte a debiter: {self.compte_a_debiter}, Compte a crediter: {self.compte_a_crediter},Beneficiaire:{self.beneficiaire}"
class VirementPermanant(models.Model):
    DEBIT = 'debit'
    CREDIT = 'credit'
    AVEC_BENEFICIAIRE = 'avec_beneficiaire'

    jour_exec=models.IntegerField()
    periodicite=models.CharField(max_length=100)
    premier_virement_annee = models.PositiveIntegerField(null=True, blank=True)
    premier_virement_mois = models.PositiveIntegerField(null=True, blank=True)
    dernier_virement_annee = models.PositiveIntegerField(null=True, blank=True)
    dernier_virement_mois = models.PositiveIntegerField(null=True, blank=True)

    compte_a_debiter = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='virements_permanents_debites')
    compte_a_crediter = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='virements_permanents_credites')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    motif_payment = models.TextField()

    beneficiaire = models.CharField(max_length=255, default='aucun')
    nom_raison_sociale = models.CharField(max_length=255, default='aucun')
    banque = models.CharField(max_length=255, default='aucun')

    def __str__(self):
        return f"Virement permanant #{self.pk} , Montant: {self.montant},Beneficiaire:{self.beneficiaire}"
    
    
 