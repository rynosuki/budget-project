from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:name>/', views.add_income, name='add_income'),
    path('..<str:name>/',views.add_income_form_submission,name='add_income_form_submission')
]