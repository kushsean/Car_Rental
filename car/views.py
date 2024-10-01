from django.shortcuts import render, redirect
from .models import *
from account.models import Account
from django.core.files.storage import FileSystemStorage
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




def home(request):

    car_all = Car.objects.all()
    car_city = []
    for i in car_all:
        car_city += Account.objects.filter(email = i.user_id)

    if request.method == 'POST':
        location = request.POST["location"]
        seat = request.POST["seat"] 
        car = [] 
        for x in Account.objects.filter(city=location):
            car += Car.objects.filter(seat=seat, user_id=x)

        return render(request, 'carlist.html', {'car':car})
    else:
        return render(request, 'index.html',{'car_city':car_city})



def carlist(request):

    car1 = Car.objects.all()
    context = {
        'car':car1,
    }
    return render(request, 'carlist.html',context)



def cardetail(request,id):

    car = Car.objects.get(id=id)
    user_id = car.user_id
    owner = Account.objects.get(email=user_id)


    context = {
        'car' : car,
        'owner' : owner,
    }

    return render(request, 'cardetail.html', context)



def carrent(request):
    if request.method == "POST":
        user = request.user
        carModel = request.POST['carModel']
        carNumber = request.POST['carNumber']
        rate = request.POST['rate']
        seat = request.POST['seat']
        description = request.POST['description']
        
        image = request.FILES['image']
        fs = FileSystemStorage()
        imagename = fs.save(image.name, image)
        url = fs.url(imagename)

        ins = Car(user_id=user, carModel=carModel, carNumber=carNumber, rate=rate, seat=seat, description=description, image=url)
        ins.save()
        return redirect('home')
    else:
        return render(request, 'carrent.html')


def booking(request):
    return render(request, 'booking.html')
