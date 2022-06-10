from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from login import settings
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from pickle import TRUE
from email import message
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes 
from django.utils.encoding import force_str 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
# from . tokens import generate_token



# Create your views here.

def home(request):
    return render(request, "authentication/index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']


        # Code for USER will not create same account 
        if User.objects.filter(username=username):
            messages.error(request, " Usernme already exist! Please try some other username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request, "Username must be under 10 characters")

        if pass1 != pass2:
            messages.error(request, "Password didn't match")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric")
            return redirect('home')


        # Code to save user details 
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False     # User account will not be activited
        myuser.save()

        messages.success(request, "Your Account has been successfully created, We have sent you a confirmation email, please confirm your email in order to activate your account.")

        #  Welcome Email

        subject ="Welcome to LANA - Django Login!!"
        message = "Hello" + myuser.first_name + "!! \n" + " Welcome to TicToe!! \n Thank you for you visiting our website\n We have also sent you a confirmation email, please confirm your email address in order to activate your account. \n\n Thanking You\n Manish Dabaria"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email] 
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        

        return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)



        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})

        else:
            messages.error(request, "Bad Credentials!!!")

            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')
