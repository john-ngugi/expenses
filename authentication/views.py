from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from django.contrib.auth.models import User 
from validate_email import validate_email 
from django.views import View 
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
# Create your views here.

class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username= data['username']

        if not str(username).isalnum():
            return JsonResponse({
                'username_error':'username should only contain alphanumeric characters',
            },status = 400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'username_error':'username already exists,choose another username',
            },status = 409)

        return JsonResponse({
                'username_valid': True,
            })
class EmailValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({
                'email_error':'the email is not valid',
            },status = 400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'email_error':'email already exists choose another email',
            },status = 409)

        return JsonResponse({
                'email_valid': True,
            })    

class registrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')    
    
    def post(self,request):
        # messages.success(request,'success whatsup success')
        # messages.info(request,'success whatsup info')
        # messages.error(request,'success whatsup error')
        # messages.warning(request,'success whatsup warning')
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context ={
            'FieldValues': request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email= email).exists():
                if len(password) < 6:
                    messages.error(request,"password too short")
                    return render(request,'authentication/register.html', context)
                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                # user.is_active = False 
                user.save()
                messages.success(request,"Account succesfully created")
                return render(request,'authentication/login.html')  
        return render(request,'authentication/register.html')  

class LoginView(View):
    def get(self,request):
        
        return render(request,'authentication/login.html')
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password :
            user = auth.authenticate(request,username = username , password = password)

            if user is not None:
                    auth.login(request,user)
                    messages.success(request,'welcome, ' + username + ", you are now logged in")
                    return redirect('expenses')
            
            messages.error(request,'Account not found')
            return render(request,'authentication/login.html')
        
        messages.error(request,'please fill all fields ')
        return render(request,'authentication/login.html')

class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,"you have been loged out")
        return redirect('login')

        
