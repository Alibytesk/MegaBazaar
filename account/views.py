from django.shortcuts import render, redirect
from django.views.generic.base import View
from account.models import User, Otp
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from account.form import LoginForm, RegisterForm, OtpCheckForm
from django.urls import reverse
from django.utils.crypto import get_random_string
from random import randint

class RegisterView(View):

    def post(self, request):
        if not request.user.is_authenticated:
            Otp.clean_otp()
            form = RegisterForm(data=request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                if not User.objects.filter(phone=cleaned_data.get('phone')).exists():
                    if Otp.objects.filter(phone=cleaned_data['phone']).exists():
                        otp = Otp.objects.get(phone=cleaned_data['phone'])
                        otp.delete()
                    token, code = get_random_string(length=255), randint(1221, 9889)
                    Otp.objects.create(code=code, token=token, phone=cleaned_data['phone'])
                    # need APIs
                    return redirect(reverse('account:otpcheck') + f'?token={token}')
                else:
                    form.add_error('phone', 'this username is already exists! ')
            return render(request, 'account/register.html', context={'form':form})
        else:
            return redirect('home:home')

    def get(self, request):
        if not request.user.is_authenticated:
            form = RegisterForm()
            return render(request, 'account/register.html', context={'form':form})
        else:
            return redirect('home:home')

class OtpCheckView(View):

    def post(self, request):
        Otp.clean_otp()
        form, token = OtpCheckForm(data=request.POST), request.GET.get('token')
        if Otp.objects.filter(token=token).exists() and not request.user.is_authenticated:
            if form.is_valid():
                cleaned_data = form.cleaned_data
                if not User.objects.filter(email=cleaned_data['email']).exists():
                    if Otp.objects.filter(code=cleaned_data['code'], token=token).exists():
                        otp = Otp.objects.get(code=cleaned_data['code'], token=token)
                        User.objects.create_user(
                            phone=otp.phone,
                            email=cleaned_data['email'],
                            password=cleaned_data['password'])
                        otp.delete()
                        return redirect('account:login')
                    else:
                        form.add_error('code', 'invalid code')
                else:
                    form.add_error('email', 'this email is already exists! ')
            return render(request, 'account/otpcheck.html', context={'form':form})
        else:
            return redirect('home:home')

    def get(self, request):
        token = request.GET.get('token')
        if Otp.objects.filter(token=token).exists() and not request.user.is_authenticated:
            form = OtpCheckForm()
            return render(request, 'account/otpcheck.html', context={'form':form})
        else:
            return redirect('home:home')

class LoginView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            form = LoginForm()
            return render(request, 'account/login.html', context={'form':form})
        else:
            return redirect('home:home')

    def post(self, request):
        if not request.user.is_authenticated:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                user = authenticate(
                    username=cleaned_data['username'],
                    password=cleaned_data['password']
                )
                if user is not None:
                    login(request, user)
                    messages.success(request,"you are now logged in")
                    return redirect('home:home')
                else:
                    form.add_error('username', 'Incorrect phone, email, password')
            else:
                form.add_error('username', 'try again')
            return render(request, 'account/login.html', context={'form':form})
        else:
            return redirect('home:home')