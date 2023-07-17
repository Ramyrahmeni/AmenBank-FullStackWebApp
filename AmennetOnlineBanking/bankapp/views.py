from django.shortcuts import render
from django.contrib import messages
from .models import utilisateur,Compte
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime





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
    last_login = datetime.now()
    if request.method == 'POST':
        user.nombre_connexions += 1
          # Update the last login time
        user.save()
        messages.success(request, "Nombre de connexions mis à jour avec succès.")

    context = {
        'user': user,
        'messages': messages.get_messages(request),
        'last_login':last_login
    }
    return render(request, 'setprfrcompteur.html', context)

def setmail(request):
    return render(request, 'setmail.html')

def setinf(request):
    return render(request, 'setinf.html')

def security(request):
    return render(request, 'security.html')

