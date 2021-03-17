from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
#from .models import Income, Expenses,Items
from databases import createDatabase

# Create your views here.

def index(request):
   return render(request, "polls/index.html")

def add_income(request, name):
    print(request)
    return render(request, "polls/add_income.html")

def add_income_form_submission(request):
    amount = request.POST["income_amount"]
    contributor = request.POST["income_contributor"]
    source = request.POST["income_source"]
    print(amount,contributor,source)

    db = createDatabase()
    db.importData(table="income", income_amount=amount,
    income_contributor=contributor, income_source=source)
    
    return render(request, "polls/add_income.html")