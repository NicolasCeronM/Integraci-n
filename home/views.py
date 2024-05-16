from django.shortcuts import render

# Create your views here.

def home(request):

    return render(request,'index.html')

def admin(request):

    return render(request,'administrador/admin.html')