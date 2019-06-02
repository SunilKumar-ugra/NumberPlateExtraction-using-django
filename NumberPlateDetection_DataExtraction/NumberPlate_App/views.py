from django.shortcuts import render
from NumberPlate_App import mail
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from NumberPlate_App.excute import Main

@csrf_exempt

def getImage(request):
    if request.method == 'GET':
        return render(request,'index.html')
    if request.method == 'POST':
        image = request.FILES['image'].name
        #print("Views",image,type(image))
        response = mail.process(image)
        print(response)
        if(response == 0):
            return render(request, 'index.html')
        else:
            return render(request,'response.html',{"r":response})

@csrf_exempt

def sendMail(request):
    if request.method == 'POST':
        print("Sending mail")
        response = mail.sendMail()
        print("Inside view",response)
        return render(request, 'index.html')
