from django.shortcuts import render
from django.contrib import messages
from .models import utilisateur,Compte,MouvementBancaire,Virement,VirementPermanant,Message_Agence,Message_Support
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db import connection
import json




# Create your views here.
def form(request):
    return render(request,"form.html")
def plus(request):
    return render(request,"plus.html")
def login(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        print(login)
        print(password)
        try:
            u = utilisateur.objects.get(login=login)
            if u.mot_de_passe == password:
                # Authentication successful
                request.session['login'] = u.login        
                u.nombre_connexions += 1
                u.last_login = datetime.now()
                u.save()
                return redirect('home')  # Redirect to home.html
            else:
                messages.error(request, 'Le mot de passe que vous avez saisi(e) n’est pas associé(e) à un compte.')
        except utilisateur.DoesNotExist:
            messages.error(request, 'Le login que vous avez saisi(e) n’est pas associé(e) à un compte.')
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")

    return render(request, 'form.html')
@login_required
def home(request):
    # Retrieve the login value from the session
    login_value = request.session.get('login')
    print(login_value)
    # Retrieve the accounts based on the login value
    accounts = Compte.objects.filter(login__login=login_value)
    s=0
    for acc in accounts:
        s+=acc.solde
    context = {
        'accounts': accounts,
        'total' : s
    }
    return render(request, 'home.html', context)
def settings(request):
    login_value = request.session.get('login')
    user = utilisateur.objects.filter(login=login_value).first()  # Retrieve the user object
    if request.method == 'POST':
        preference_linguistique = request.POST.get('langue')
        user.preference_linguistique = preference_linguistique
        user.save()
        messages.success(request, 'Préférences linguistiques mises à jour avec succès.')
    context = {
        'user': user,
        'messages': messages.get_messages(request),  # Include messages in the context
    }

    
    return render(request, 'set.html', context)
def setprfr(request):
    login_value = request.session.get('login')
    user = utilisateur.objects.get(login=login_value)
    accounts = Compte.objects.filter(login__login=login_value)
    if request.method == 'POST':
        selected_account_num = request.POST.get('default-account')
        user.compte_par_defaut = selected_account_num
        
        user.save()
        messages.success(request, 'Compte par defaut mise à jour avec succès.')

    context = {
        'accounts': accounts,
        'messages': messages.get_messages(request),  # Include messages in the context

    }
    return render(request, 'setprfr.html', context)
def setprfrlib(request):
    login_value = request.session.get('login')
    accounts = Compte.objects.filter(login__login=login_value)
    if request.method == 'POST':
        for account in accounts:
            account_label = request.POST.get(f"account-label-{account.num_compte}")
            print(account_label)
            account.libelle = account_label
            account.save()
        messages.success(request, "Les libelles de compte sont mises a jour.")

    context = {
        'accounts': accounts,
        'messages' :messages.get_messages(request), 
    }
    return render(request, 'setprfrlib.html',context)

def setprfrmail(request):
    login_value = request.session.get('login')
    accounts = Compte.objects.filter(login__login=login_value)
    
    if request.method == 'POST':
        for account in accounts:
            checkbox_name = f"alert-mail-{account.num_compte}"
            alert_mail_value = request.POST.get(checkbox_name)
            account.alerte_mail = alert_mail_value
            account.save()
        
        messages.success(request, "Alerte Mail mise a jour avec succes.")

    context = {
        'accounts': accounts,
        'messages': messages.get_messages(request),
    }
    return render(request, 'setprfrmail.html', context)



def setprfrsms(request):
    login_value = request.session.get('login')
    accounts = Compte.objects.filter(login__login=login_value)
    
    if request.method == 'POST':
        for account in accounts:
            checkbox_name = f"alert-mail-{account.num_compte}"
            alert_sms_value = request.POST.get(checkbox_name)
            account.alerte_sms = alert_sms_value
            account.save()
        
        messages.success(request, "Alerte SMS mise a jour avec succes.")

    context = {
        'accounts': accounts,
        'messages': messages.get_messages(request),
    }
    return render(request, 'setprfrsms.html', context)

def setprfrcompteur(request):
    login_value = request.session.get('login')
    user = utilisateur.objects.get(login=login_value)
    last_login = user.last_login

    context = {
        'user': user,
        'messages': messages.get_messages(request),
        'last_login':last_login
    }
    return render(request, 'setprfrcompteur.html', context)

def setmail(request):
    return render(request, 'setmail.html')

def setinf(request):
    login_value = request.session.get('login')
    accounts = Compte.objects.filter(login__login=login_value)
    context = {
        'accounts': accounts,
    }
    return render(request, 'setinf.html',context)

from django.contrib import messages

def security(request):
    login_value = request.session.get('login')
    user = utilisateur.objects.get(login=login_value)
    if request.method == 'POST':
        user = utilisateur.objects.get(login=login_value)
        old = request.POST.get('old')
        if old == user.mot_de_passe:
            new1 = request.POST.get('new')
            new2 = request.POST.get('confirm')
            if new1 == new2:
                user.mot_de_passe = new1
                user.save()
                messages.success(request, 'Mot de passe mis à jour avec succès.')
            else:
                messages.error(request, 'Les mots de passe ne sont pas identiques.')
        else:
 
            messages.error(request, 'Mot de passe incorrect')

    context = {
        'user': user,
        'messages': messages.get_messages(request),
    }
    return render(request, 'security.html', context)
 


def recherchemouvement_view(request):
    login_value = request.session.get('login')
    accounts = Compte.objects.filter(login__login=login_value)

    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        type = request.POST.get('type')
        mntmin = request.POST.get('mntmin')
        mntmax = request.POST.get('mntmax')
        datemin = request.POST.get('datemin')
        datemax = request.POST.get('datemax')
        print(account_number)
        print(type)

        # Construct the search query
        query = {}
        if account_number:
            query['compte__num_compte'] = account_number
        if type:
            type = type.lower()
            if type in ['debit', 'débit']:
                query['type__iexact'] = 'debit'
            elif type in ['credit', 'crédit']:
                query['type__iexact'] = 'credit'
        if mntmin:
            query['montant__gte'] = mntmin
        if mntmax:
            query['montant__lte'] = mntmax
        if datemin and datemax:
            query['date__range'] = [datemin, datemax]

        # Perform the search
        results = MouvementBancaire.objects.filter(**query)

        context = {
            'results': results,
            'accounts': accounts
        }
        print(results)
        return render(request, 'recherchemouvement.html', context)
    return render(request, 'recherchemouvement.html',{'accounts':accounts})

def mvmparop_view(request):
    login_value = request.session.get('login')
    accounts = Compte.objects.filter(login__login=login_value)
    
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        display_option = request.POST.get('display_options')
        acc=Compte.objects.filter(num_compte=account_number)
        ch=request.method
        acc=acc[0]
        print(acc)
        solde=acc.solde
        # Retrieve movements for the selected accounts
        movements = MouvementBancaire.objects.filter(compte__num_compte=account_number).order_by('date')
        # Prepare data for the chart
        moves=[]
        for i in movements:
            montant=float(i.montant)
            type=i.type
            if(type=='debit' or type=='Débit'):
                moves.append(-1*montant)
            else:
                moves.append(montant)
        data=[]
        print(solde)
        print(moves)
        data.append(solde)
        reversed_moves = moves[::-1]
        for i in range(len(moves)-1):
            data.insert(0,solde-reversed_moves[i])
            solde-=reversed_moves[i]
        labels = [movement.date.strftime('%Y-%m-%d') for movement in movements]
        print(labels)
        print(data)
        chart_data = {'labels': labels, 'data': data}

        context = {
            'accounts': accounts,
            'account_number': account_number,
            'display_option': display_option,
            'movements': movements,
            'chart_data': json.dumps(chart_data),  # Convert data to JSON format
            'ch':ch
        }
        print('rendered')
        return render(request, 'mvmparop.html', context)

    context = {
        'accounts': accounts,
    }
    return render(request, 'mvmparop.html', context)

def cfonbparcompteparperiode_view(request):
    login_value = request.session.get('login')
    accounts = Compte.objects.filter(login__login=login_value)
    context = {
        'accounts': accounts,
    }
    return render(request, 'cfonbparcompteparperiode.html',context)

def cfonbhis_view(request):
    login_value = request.session.get('login')
    accounts = Compte.objects.filter(login__login=login_value)
    context = {
        'accounts': accounts,
    }
    return render(request, 'cfonbhis.html',context)

def cfonbhisglobal_view(request):
    login_value = request.session.get('login')
    accounts = Compte.objects.filter(login__login=login_value)
    context = {
        'accounts': accounts,
    }
    return render(request, 'cfonbhisglobal.html',context)
def virement(request):
    login_value = request.session.get('login')
    accounts = Compte.objects.filter(login__login=login_value)
    context = {
        'accounts': accounts,
    }
    if request.method == 'POST':
        compte_a_crediter_num = request.POST.get('account_number_credit')
        compte_a_debiter_num = request.POST.get('account_number_debit')
        montant = request.POST.get('montant')
        date_execution = request.POST.get('date')
        motif_payment = request.POST.get('message')

        # Get the Compte instances for compte_a_crediter and compte_a_debiter
        compte_a_crediter = Compte.objects.get(num_compte=compte_a_crediter_num)
        compte_a_debiter = Compte.objects.get(num_compte=compte_a_debiter_num)

        # Create a new Virement object and save it to the database
        virement = Virement(
            compte_a_crediter=compte_a_crediter,
            compte_a_debiter=compte_a_debiter,
            montant=montant,
            date_execution=date_execution,
            motif_payment=motif_payment  # Change this based on your logic for determining the type
        )
        virement.save()

        # Add a success message to be displayed on the redirected page
        messages.success(request, 'Virement enregistré.')

        # Redirect to the same page after saving the data
        return render(request,'virement.html',{'accounts': accounts,'messages':messages.get_messages(request)})

    # If it's a GET request, just render the template with the form
    return render(request, 'virement.html', context)
def virmentsigne_view(request):
    return render(request, 'virmentsigne.html')

def virhis_view(request):
    return render(request, 'virhis.html')

def virben_view(request):
    login_value = request.session.get('login')
    accounts = Compte.objects.filter(login__login=login_value)
    context = {
        'accounts': accounts,
    }
    if request.method == 'POST':
        compte_a_crediter_num = request.POST.get('account_number_credit')
        compte_a_debiter_num = request.POST.get('account_number_debit')
        montant = request.POST.get('montant')
        date_execution = request.POST.get('date')
        motif_payment = request.POST.get('message')
        ben=request.POST.get('ben')
        raison=request.POST.get('raison')
        banque=request.POST.get('banque')
        # Get the Compte instances for compte_a_crediter and compte_a_debiter
        compte_a_crediter = Compte.objects.get(num_compte=compte_a_crediter_num)
        compte_a_debiter = Compte.objects.get(num_compte=compte_a_debiter_num)

        # Create a new Virement object and save it to the database
        virement = Virement(
            compte_a_crediter=compte_a_crediter,
            compte_a_debiter=compte_a_debiter,
            montant=montant,
            date_execution=date_execution,
            motif_payment=motif_payment,
            beneficiaire=ben,
            nom_raison_sociale=raison,
            banque=banque,
        )
        virement.save()

        # Add a success message to be displayed on the redirected page
        messages.success(request, 'Virement enregistré.')

        # Redirect to the same page after saving the data
        return render(request,'virben.html',{'accounts': accounts,'messages':messages.get_messages(request)})

    # If it's a GET request, just render the template with the form
    return render(request, 'virben.html', context)

def virbenges_view(request):
    return render(request, 'virbenges.html')

def virbensin_view(request):
    return render(request, 'virbensin.html')

def virbenhis_view(request):
    return render(request, 'virbenhis.html')

def virmas_view(request):
    return render(request, 'virmas.html')

def virmassin_view(request):
    return render(request, 'virmassin.html')

def virmashis_view(request):
    return render(request, 'virmashis.html')

def virper_view(request):
    login_value = request.session.get('login')
    accounts = Compte.objects.filter(login__login=login_value)
    context = {
        'accounts': accounts,
    }
    if request.method == 'POST':
        compte_a_crediter_num = request.POST.get('account_number_credit')
        compte_a_debiter_num = request.POST.get('account_number_debit')
        montant = request.POST.get('montant')
        jrex=request.POST.get('jrex')
        prd=request.POST.get('prd')
        premiermois=request.POST.get('premiermois')
        premierannee=request.POST.get('premierannee')
        derniermois=request.POST.get('derniermois')
        dernierannee=request.POST.get('dernierannee')
        motif_payment = request.POST.get('message')
        # Get the Compte instances for compte_a_crediter and compte_a_debiter
        compte_a_crediter = Compte.objects.get(num_compte=compte_a_crediter_num)
        compte_a_debiter = Compte.objects.get(num_compte=compte_a_debiter_num)

        # Create a new Virement object and save it to the database
        virement = VirementPermanant(
            compte_a_crediter=compte_a_crediter,
            compte_a_debiter=compte_a_debiter,
            montant=montant,
            jour_exec=jrex,
            periodicite=prd,
            premier_virement_annee=premierannee,
            premier_virement_mois=premiermois,
            dernier_virement_annee=dernierannee,
            dernier_virement_mois=derniermois,
            motif_payment=motif_payment,
        )
        virement.save()

        # Add a success message to be displayed on the redirected page
        messages.success(request, 'Virement permanant enregistré.')

        # Redirect to the same page after saving the data
        return render(request,'virper.html',{'accounts': accounts,'messages':messages.get_messages(request)})

    # If it's a GET request, just render the template with the form
    return render(request, 'virper.html', context)

def virperben_view(request):
    login_value = request.session.get('login')
    accounts = Compte.objects.filter(login__login=login_value)
    context = {
        'accounts': accounts,
    }
    if request.method == 'POST':
        compte_a_crediter_num = request.POST.get('account_number_credit')
        compte_a_debiter_num = request.POST.get('account_number_debit')
        montant = request.POST.get('montant')
        jrex=request.POST.get('jrex')
        prd=request.POST.get('prd')
        premiermois=request.POST.get('premiermois')
        premierannee=request.POST.get('premierannee')
        derniermois=request.POST.get('derniermois')
        dernierannee=request.POST.get('dernierannee')
        motif_payment = request.POST.get('message')
        ben=request.POST.get('ben')
        raison=request.POST.get('raison')
        banque=request.POST.get('banque')
        # Get the Compte instances for compte_a_crediter and compte_a_debiter
        compte_a_crediter = Compte.objects.get(num_compte=compte_a_crediter_num)
        compte_a_debiter = Compte.objects.get(num_compte=compte_a_debiter_num)

        # Create a new Virement object and save it to the database
        virement = VirementPermanant(
            compte_a_crediter=compte_a_crediter,
            compte_a_debiter=compte_a_debiter,
            montant=montant,
            jour_exec=jrex,
            periodicite=prd,
            premier_virement_annee=premierannee,
            premier_virement_mois=premiermois,
            dernier_virement_annee=dernierannee,
            dernier_virement_mois=derniermois,
            motif_payment=motif_payment,
            beneficiaire=ben,
            nom_raison_sociale=raison,
            banque=banque
        )
        virement.save()

        # Add a success message to be displayed on the redirected page
        messages.success(request, 'Virement Permanant enregistré.')

        # Redirect to the same page after saving the data
        return render(request,'virperben.html',{'accounts': accounts,'messages':messages.get_messages(request)})

    # If it's a GET request, just render the template with the form
    return render(request, 'virperben.html', context)
def virperlis_view(request):
    return render(request, 'virperlis.html')

def virpersin_view(request):
    return render(request, 'virpersin.html')

def modvir_view(request):
    return render(request, 'modvir.html')
def mon_view(request):
    return render(request, 'mon.html')

def monrech_view(request):
    return render(request, 'monrech.html')

def mondeb_view(request):
    return render(request, 'mondeb.html')

def monopp_view(request):
    return render(request, 'monopp.html')

def ouverture_lc_view(request):
    # Add your logic for OuvertureLC view here
    return render(request, 'tele.html')

def transfert_emis_tre_view(request):
    # Add your logic for Transfert emis - TRE view here
    return render(request, 'telete.html')

def transfert_recus_trr_view(request):
    # Add your logic for Transfert recus - TRR view here
    return render(request, 'teletr.html')

def avis_operation_pdf_view(request):
    # Add your logic for Avis d'opération (PDF) view here
    return render(request, 'teleaop.html')

def avis_operation_text_view(request):
    # Add your logic for Avis d'opération (text) view here
    return render(request, 'teleaot.html')

def situation_effets_view(request):
    # Add your logic for Situation des effets view here
    return render(request, 'telees.html')

def cro_effet_structured_view(request):
    # Add your logic for CRO effet structuré view here
    return render(request, 'telecro.html')

def releve_compte_pdf_view(request):
    # Add your logic for Relevé de compte (PDF) view here
    return render(request, 'telercp.html')

def releve_compte_text_view(request):
    # Add your logic for Relevé de compte (text) view here
    return render(request, 'telerct.html')

def releve_compte_cfonb_view(request):
    # Add your logic for Relevé de compte (CFONB) view here
    return render(request, 'telercc.html')

def echelle_interets_pdf_view(request):
    # Add your logic for Echelle d'intérêts (PDF) view here
    return render(request, 'teleeip.html')

def echelle_interets_text_view(request):
    # Add your logic for Echelle d'intérêts (text) view here
    return render(request, 'teleeit.html')

def image_cheques_view(request):
    # Add your logic for Image des chèques view here
    return render(request, 'teleic.html')

def image_lettres_change_view(request):
    # Add your logic for Image des lettres de change view here
    return render(request, 'teleil.html')

def situation_cartes_view(request):
    # Add your logic for Situation des cartes view here
    return render(request, 'telescard.html')

def situation_credits_view(request):
    # Add your logic for Situation des crédits view here
    return render(request, 'telescred.html')

def situation_placements_view(request):
    # Add your logic for Situation des placements view here
    return render(request, 'telesplac.html')

def sort_cheques_verse_view(request):
    # Add your logic for Sort des chèques versés view here
    return render(request, 'telesorcheq.html')

def transactions_tpe_view(request):
    # Add your logic for Transactions TPE view here
    return render(request, 'teletrantpe.html')

def divers_view(request):
    # Add your logic for Divers view here
    return render(request, 'teled.html')
def rediger_message_agence(request):
    login_value = request.session.get('login')
    user = utilisateur.objects.get(login=login_value)
    if request.method == 'POST':
        agence=request.POST.get('agence')
        objet = request.POST.get('objet')
        numtel=request.POST.get('numtel')
        msg=request.POST.get('message')
        u = utilisateur.objects.get(login=login_value)
        m = Message_Agence(
            login=u,
            objet=objet,
            numero_tel=numtel,
            message=msg,
            agence=agence,
        )
        m.save()

        # Add a success message to be displayed on the redirected page
        messages.success(request, 'Message envoyé.')

        # Redirect to the same page after saving the data
        return render(request,'mes.html',{'user': user,'messages':messages.get_messages(request)})
    context={'user':user}
    return render(request, 'mes.html',context)

def rediger_message_support(request):
    login_value = request.session.get('login')
    user = utilisateur.objects.get(login=login_value)
    # Add your logic for Rediger un message au support view here
    if request.method == 'POST':
        numtel = request.POST.get('numtel')
        numfax = request.POST.get('numfax')
        sysex = request.POST.get('sysex')
        srvpak = request.POST.get('srvpak')
        navigateur = request.POST.get('navigateur')
        frnsaccess = request.POST.get('frnsaccess')
        communication = request.POST.get('communication')
        meserr = request.POST.get('meserr')

            # Save the form data to the Message_Support model
        m = Message_Support(
                login=user,
                numero_tel=numtel,
                numero_fax=numfax,
                system_exploitation=sysex,
                service_pack=srvpak,
                navigateur=navigateur,
                fournisseur_internet=frnsaccess,
                communication=communication,
                message_erreur=meserr,
            )
        m.save()
            # Add a success message to be displayed on the redirected page
        messages.success(request, 'Message envoyé au support.')
            # Redirect to the same page after saving the data
        return render(request,'messuppo.html',{'user': user,'messages':messages.get_messages(request)})
    context={'user':user}
    return render(request, 'messuppo.html',context)
def messages_recus(request):
    # Add your logic for Messages recus view here
    return render(request, 'mesrec.html')

def messages_envoyes(request):
    login_value = request.session.get('login')
    messagence = Message_Agence.objects.filter(login__login=login_value)
    messupport=Message_Support.objects.filter(login__login=login_value)
    context={'messages_agences':messagence,'messages_support':messupport}
    # Add your logic for Messages envoyes view here
    return render(request, 'mesenv.html',context)

def messages_en_instance(request):
    # Add your logic for Messages en instance view here
    return render(request, 'mesins.html')

def messages_supprimes(request):
    # Add your logic for Messages supprimes view here
    return render(request, 'messupp.html')
def fin(request):
    return render(request,'fin.html')
def cd(request):
    return render(request,'cd.html')
def finsc(request):
    return render(request,'finsc.html')
def cbam(request):
    return render(request,'cbam.html')
def cs(request):
    return render(request,'cs.html')
def cb(request):
    return render(request,'cb.html')
def gb(request):
    return render(request,'gb.html')
def gbc(request):
    return render(request,'gbc.html')
def gbdr(request):
    return render(request,'gbdr.html')
def gbed(request):
    return render(request,'gbed.html')
def services_view(request):
    # Your view logic here...
    return render(request, 'services.html')

def spi_view(request):
    # Your view logic here...
    return render(request, 'spi.html')

def sst_view(request):
    # Your view logic here...
    return render(request, 'sst.html')

def scch_view(request):
    # Your view logic here...
    return render(request, 'scch.html')

def sdc_view(request):
    # Your view logic here...
    return render(request, 'sdc.html')

def sdml_view(request):
    # Your view logic here...
    return render(request, 'sdml.html')

def sdd_view(request):
    # Your view logic here...
    return render(request, 'sdd.html')
def ordre_virement_view(request):
    # Your view logic here...
    return render(request, 'etr.html')

def transfert_emis_signer_view(request):
    # Your view logic here...
    return render(request, 'etrsin.html')

def historique_transferts_emis_view(request):
    # Your view logic here...
    return render(request, 'etrhis.html')

def ouverture_lettre_credit_view(request):
    # Your view logic here...
    return render(request, 'etrcrd.html')

def lettres_credit_signer_view(request):
    # Your view logic here...
    return render(request, 'etrcrdsin.html')

def historique_lettres_credit_view(request):
    # Your view logic here...
    return render(request, 'etrcrdhis.html')