from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from notes.models import Notes
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from .models import EmailConfirm

User = get_user_model()



def send_email_confirmation(user):
    code = randint(100000, 999999)
    email_confirm = EmailConfirm.objects.update_or_create(user=user, defaults={'code': str(code)})
    try:
        send_mail(
            subject='Email confirmation',
            message=f'Mr(s) {user.username} welcome tpo our dangerous web application plz confirm ur email its ur code {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]

        )
    except Exception as e:
        print(e, '====================================')


def register_view(request):
    if request.method =='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not email or not password1:
            return render(request, 'accounts/register.html', {'error':'All fields are necessery'})

        if password1!=password2:
            return render(request, 'accounts/register.html', {'error':'Passwords doesnt match'})
        elif User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error':'Username already exists'})
        elif User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {'error':'Email already exists'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password2,
            is_active=False,
        )
        send_email_confirmation(user)
        return render(request, 'accounts/confirm.html', {'user':user})
            
    return render(request, 'accounts/register.html')


def confirm_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')    

        user = User.objects.filter(email=email).first()
        if not user:
            return render(request, 'accounts/confirm.html', {'error': 'Wrond email or code'})
        
        if code != code:
            return render(request, 'accounts/confirm.html', {'error': 'Wrond  code'})

        user.is_active = True
        user.save()
        return redirect('login')

    return render(request, 'accounts/confirm.html')




def login_view(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')    

        user = authenticate(request, username=username, password=password)

        if not user:
            not_active = User.objects.filter(username=username, is_active=False)
            if not_active:
                return redirect('confirm')
            
            return render(request, 'accounts/login.html', {'error':'Password or Usernames is not correct!'})

        login(request, user=user) 
        return redirect('notes')
     
    return render(request, 'accounts/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')


