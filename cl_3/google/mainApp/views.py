from django.shortcuts import render
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    messages.success(request, "Logged In Successfully!")
    return render(request, 'dashboard.html')

@login_required
def home(request):
    return render(request, 'home.html')