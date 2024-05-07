from django.shortcuts import render

# create user
from django.contrib.auth.models import User

# Authenticate user
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Adding messages to a call
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.

def index(request):
    # check if a user is anynomous(user who is not logged in)
    # print(request.user.is_anonymous)
    if request.user.is_anonymous:
        print("not logged")
        return render(request, 'index.html')

    return render(request, 'dashboard.html')

def dashboard(request):
    return render(request, 'dashboard.html')


def signUpUser(request):
    if (request.user.is_anonymous and request.method!="POST"):
        return render(request, 'signup.html')

    elif (request.user.is_anonymous and request.method=="POST"):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # authenticate if the user already exists or not
        user = authenticate(email = email)
        if user is not None:
            # user already exists
            messages.warning(request, "User already exists! Please Login to Your account")

            # redirect to the sign up page
            return redirect('/home/login/')
        else:
            # this is a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account Created! Login Again")
            return redirect('/home/login/')
    return render(request, 'dashboard.html')




def loginUser(request):
    if (request.user.is_anonymous and request.method!="POST"):
        return render(request, 'login.html')

    elif (request.user.is_anonymous and request.method=="POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            messages.success(request, "Logged In Successfully!")
            return redirect('/home/dashboard/')

        else:
            # No backend authenticated the credentials
            messages.success(request, "Invalid Credentials!")
            return redirect('/home/login/')
    return render(request, 'dashboard.html')

@login_required
def logoutUser(request):
    logout(request)
    return redirect('/')


def videoCall(request):
    return render(request,'videocall.html',{'name':request.user.username})

@login_required
def joinRoom(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect(roomID)
    return render(request, 'joinroom.html')
    # return render(request,'joinroom.html',{'name':request.user.username})
