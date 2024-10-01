from django.shortcuts import render, redirect
from .models import Account
from django.contrib.auth.models import auth
from django.contrib import messages
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient


def index(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0713956407'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://darajambili.herokuapp.com/express-payment';
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

def stk_push_callback(request):
        data = request.body
        
        return HttpResponse("STK Push in Django👋")



def profile_page(request):
    if request.user.is_authenticated:
        
        return render(request, "profile-page.html", {})
    else:
        return redirect('login') 


def register(request):
    if request.method == 'POST':
        first_name 		        = request.POST['first_name']
        last_name 		        = request.POST['last_name']
        email_id                = request.POST['email_id']
        username 	         	= request.POST['username']
        password                = request.POST['password']
        confirm_password        = request.POST['confirm_password']
        city                    = request.POST['city']
        address                 = request.POST['address']
        phone_number            = request.POST['phone_number']

        if password==confirm_password:
            if Account.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect('register')
            elif Account.objects.filter(email=email_id).exists():
                messages.info(request, 'Account with specified email already exists')
                return redirect('register')
            else:
                user = Account.objects.create_user(
                        email=email_id, 
                        first_name=first_name, 
                        last_name=last_name, 
                        username=username, 
                        city=city, 
                        address=address, 
                        phone_number=phone_number, 
                        password=password
                    )
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords not matching')
            return redirect('register')

    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email_id    = request.POST['email_id']
        password    = request.POST['password']
        user = auth.authenticate(email=email_id, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

    
def logout(request):
    auth.logout(request)
    return redirect('home')