from django.contrib import admin
from django.urls import path,include
from mybot import views

urlpatterns = [
    # directly comes here as home page
    path("",view=views.home,name='home')
]
