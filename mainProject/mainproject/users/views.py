from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

class custormUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email",]

# Create your views here.   

def home(request):
    return render(request,'users/html/home.html')

def signup(request):
    if request.method=='POST':
        form = custormUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Congratulations! Registration successfull!')
        else:
            context = {
                "form":form,
            }
            return render(request,'users/html/signUp.html',context=context)
    else:
        form = custormUserCreationForm()
        context = {
            "form":form,
        }
        return render(request,'users/html/signUp.html',context=context)
    

def Login(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('profile')
        else:
            form = AuthenticationForm()
            context = {
                "form" : form,
            }
            return render(request,'users/html/login.html',context)
    else:
        form = AuthenticationForm()
        context = {
            "form" : form,
        }
        return render(request,'users/html/login.html',context)
    
@login_required
def Logout(request):
    logout(request)
    return redirect('home')