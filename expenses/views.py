from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category,Expense
from django.contrib import messages
from django.shortcuts import redirect 
from django.core.paginator import Paginator
import json 
from django.http import JsonResponse
from userpreferences.models import UserPreference

# Create your views here.

def search_expenses(request):
    if request.method =='POST':
        search_string = json.loads(request.body).get('searchText')
        
        expenses = Expense.objects.filter(amount__istartswith= search_string,owner=request.user) | Expense.objects.filter(date__istartswith = search_string,owner=request.user) | Expense.objects.filter(description__istartswith = search_string,owner=request.user) | Expense.objects.filter(category__istartswith = search_string,owner=request.user)
        
        data = expenses.values()

        return JsonResponse(list(data), safe=False) 
    
@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses,4)
    page_number =  request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if UserPreference.objects.filter(user = request.user).exists():
        currency = UserPreference.objects.get(user = request.user).currency
    else:
        currency = 'KES - Kenyan Shilling'
    context = {
    'expenses':expenses, 
    'page_obj':page_obj,
    'currency': currency
    }
    return render(request,'index.html',context)
    

def addExpense(request):
    categories = Category.objects.all()
    context = {
        'categories':categories,
        'values':request.POST,
    }
    if request.method =='GET':
        return render(request,'add_expense/add_expense.html',context)

    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request,"Amount is required")
            return render(request,'add_expense/add_expense.html',context)
        
        description = request.POST['description']
        if not description:
            messages.error(request,"description is required")
            return render(request,'add_expense/add_expense.html',context)
        
        date = request.POST['date']
        if not date:
            messages.error(request,"date is required")
            return render(request,'add_expense/add_expense.html',context)    
        
        category = request.POST['category']
        if not category:
            messages.error(request,"category is required")
            return render(request,'add_expense/add_expense.html',context)    

        Expense.objects.create(owner=request.user,amount=amount,date=date,category=category,description=description)
        messages.success(request,'expense saved successfully')

        return redirect('expenses')

def expense_edit(request,id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense':expense,
        'categories':categories,
        'values':expense,
    }
    if request.method == 'GET':
        return render(request, 'add_expense/edit-expense.html',context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request,"Amount is required")
            return render(request,'add_expense/edit-expense.html',context)
        
        description = request.POST['description']
        if not description:
            messages.error(request,"description is required")
            return render(request,'add_expense/edit-expense.html',context)
        
        date = request.POST['date']
        if not date:
            messages.error(request,"date is required")
            return render(request,'add_expense/edit-expense.html',context)    
        
        category = request.POST['category']
        if not category:
            messages.error(request,"category is required")
            return render(request,'add_expense/edit-expense.html',context)    

        
        expense.owner = request.user 
        expense.amount = amount
        expense.category =category
        expense.date = date 
        expense.description = description
        
        expense.save()
        messages.success(request,'expense updated successfully')

        return redirect('expenses')
    
def delete_expense(request, id ):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request,'expense deleted successfully')
    return redirect('expenses')