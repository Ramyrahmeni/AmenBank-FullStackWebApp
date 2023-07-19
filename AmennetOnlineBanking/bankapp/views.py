from django.shortcuts import render
from django.contrib import messages
from .models import utilisateur,Compte,MouvementBancaire,Virement,VirementPermanant
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
                messages.success(request, "Nombre de connexions mis à jour avec succès.")
                return redirect('home')  # Redirect to home.html
            else:
                messages.error(request, 'Invalid password')
        except utilisateur.DoesNotExist:
            messages.error(request, 'Invalid login')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'form.html')
@login_required
def home(request):
    # Retrieve the login value from the session
    login_value = request.session.get('login')
    print(login_value)
    # Retrieve the accounts based on the login value
    accounts = Compte.objects.filter(login__login=login_value)
    
    context = {
        'accounts': accounts,
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
        print(display_option)
        # Retrieve movements for the selected accounts
        movements = MouvementBancaire.objects.filter(compte__num_compte=account_number).order_by('date')
        # Prepare data for the chart
        labels = [movement.date.strftime('%Y-%m-%d') for movement in movements]
        data = [float(movement.montant) for movement in movements]
        print(labels)
        print(data)
        chart_data = {'labels': labels, 'data': data}

        context = {
            'accounts': accounts,
            'account_number': account_number,
            'display_option': display_option,
            'movements': movements,
            'chart_data': json.dumps(chart_data),  # Convert data to JSON format
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
