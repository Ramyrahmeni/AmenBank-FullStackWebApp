from django.contrib import admin
from .models import utilisateur,Compte,MouvementBancaire,VirementPermanant,Virement,Message_Agence,Message_Support

# Register your models here.
# Register your models here.
admin.site.register(utilisateur)
admin.site.register(Compte)
admin.site.register(MouvementBancaire)
admin.site.register(VirementPermanant)
admin.site.register(Virement)
admin.site.register(Message_Agence)
admin.site.register(Message_Support)
