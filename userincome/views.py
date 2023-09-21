from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Source,UserIncome
from django.contrib import messages
from django.shortcuts import redirect 
from django.core.paginator import Paginator
import json 
from django.http import JsonResponse
from userpreferences.models import UserPreference

# Create your views here.

def search_incomes(request):
    if request.method =='POST':
        search_string = json.loads(request.body).get('searchText')
        
        incomes = UserIncome.objects.filter(amount__istartswith= search_string,owner=request.user) | UserIncome.objects.filter(date__istartswith = search_string,owner=request.user) | UserIncome.objects.filter(description__istartswith = search_string,owner=request.user) | UserIncome.objects.filter(source__istartswith = search_string,owner=request.user)
        
        data = incomes.values()

        return JsonResponse(list(data), safe=False) 
    
@login_required(login_url='/authentication/login')
def index(request):
    categories = Source.objects.all()
    incomes = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(incomes,4)
    page_number =  request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if UserPreference.objects.filter(user = request.user).exists():
        currency = UserPreference.objects.get(user = request.user).currency
    else:
        currency = 'KES - Kenyan Shilling'
    context = {
    'incomes':incomes, 
    'page_obj':page_obj,
    'currency': currency
    }
    return render(request,'index.html',context)

def addincome(request):
    categories = Source.objects.all()
    context = {
        'categories':categories,
        'values':request.POST,
    }
    if request.method =='GET':
        return render(request,'add_income/add_income.html',context)

    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request,"Amount is required")
            return render(request,'add_income/add_income.html',context)
        
        description = request.POST['description']
        if not description:
            messages.error(request,"description is required")
            return render(request,'add_income/add_income.html',context)
        
        date = request.POST['date']
        if not date:
            messages.error(request,"date is required")
            return render(request,'add_income/add_income.html',context)    
        
        source = request.POST['source']
        if not source:
            messages.error(request,"source is required")
            return render(request,'add_income/add_income.html',context)    

        UserIncome.objects.create(owner=request.user,amount=amount,date=date,source=source,description=description)
        messages.success(request,'income saved successfully')

        return redirect('incomes')

def income_edit(request,id):
    income = income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income':income,
        'sources':sources,
        'values':income,
    }
    if request.method == 'GET':
        return render(request, 'add_income/edit-income.html',context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request,"Amount is required")
            return render(request,'add_income/edit-income.html',context)
        
        description = request.POST['description']
        if not description:
            messages.error(request,"description is required")
            return render(request,'add_income/edit-income.html',context)
        
        date = request.POST['date']
        if not date:
            messages.error(request,"date is required")
            return render(request,'add_income/edit-income.html',context)    
        
        source = request.POST['source']
        if not source:
            messages.error(request,"source is required")
            return render(request,'add_income/edit-income.html',context)    

        
        income.owner = request.user 
        income.amount = amount
        income.category =source
        income.date = date 
        income.description = description
        
        income.save()
        messages.success(request,'income updated successfully')

        return redirect('incomes')
    
def delete_income(request, id ):
    income = income.objects.get(pk=id)
    income.delete()
    messages.success(request,'income deleted successfully')
    return redirect('incomes')