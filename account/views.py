from django.shortcuts import render, redirect
from django.views.generic.base import View
from account.models import User, Otp
from django.contrib.auth import mixins, authenticate, login, logout
from django.contrib import messages
from account.form import LoginForm, RegisterForm, OtpCheckForm, ChangePasswordForm, ForgotPasswordForm, SetPasswordForm
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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
            return render(request, 'account/register.html', context={'form': form})
        else:
            return redirect('home:home')

    def get(self, request):
        if not request.user.is_authenticated:
            form = RegisterForm()
            return render(request, 'account/register.html', context={'form': form})
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
            return render(request, 'account/otpcheck.html', context={'form': form})
        else:
            return redirect('home:home')

    def get(self, request):
        token = request.GET.get('token')
        if Otp.objects.filter(token=token).exists() and not request.user.is_authenticated:
            form = OtpCheckForm()
            return render(request, 'account/otpcheck.html', context={'form': form})
        else:
            return redirect('home:home')


class LoginView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            form = LoginForm()
            return render(request, 'account/login.html', context={'form': form})
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
                    messages.success(request, "you are now logged in")
                    return redirect('home:home')
                else:
                    form.add_error('username', 'Incorrect phone, email, password')
            else:
                form.add_error('username', 'try again')
            return render(request, 'account/login.html', context={'form': form})
        else:
            return redirect('home:home')


class LogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, 'you are logged out')
        return redirect('home:home')


class ChangePasswordView(mixins.LoginRequiredMixin, View):

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'account/change_password.html', context={'form':ChangePasswordForm()})
        else:
            return redirect('account:login')

    def post(self, request):
        if request.user.is_authenticated:
            form = ChangePasswordForm(data=request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                if cleaned_data.get('password1') == cleaned_data.get('confirm_password'):
                    user = User.objects.get(phone=request.user.phone)
                    if user.check_password(cleaned_data['current_password']):
                        user.set_password(cleaned_data.get('password1'))
                        user.save()
                        messages.success(request, 'Password updated successfully.')
                        return redirect('home:home')
                    else:
                        form.add_error('current_password', 'please enter current password')
                else:
                    form.add_error('password1', 'password does not Match')
            return render(request, 'account/change_password.html', context={'form':form})
        else:
            return redirect('account:login')

class ForgotPasswordView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'account/forgot_password.html', context={'form':ForgotPasswordForm()})
        else:
            return redirect('home:home')

    def post(self, request):
        if not request.user.is_authenticated:
            form = ForgotPasswordForm(data=request.POST)
            if form.is_valid():
                if User.objects.filter(email=form.cleaned_data['email']).exists():
                    user = User.objects.get(email__exact=form.cleaned_data['email'])
                    email_subject = 'reset your password'
                    message = render_to_string('account/reset_password_email.html'
                                               ,{
                            'user':user,
                            'domain':get_current_site(request),
                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                            'token':default_token_generator.make_token(user),
                                               })
                    send_email = EmailMessage(email_subject, message, to=[form.cleaned_data['email']])
                    send_email.send()
                    messages.success(request, 'Password reset email has been sent to your email address')
                    return redirect('account:login')
                else:
                    form.add_error('email', 'this Email is not exists')
            return render(request, 'account/forgot_password.html', context={'form':form})
        else:
            return redirect('home:home')

class ResetPassword(View):

    def get(self, request, uidb64, token):
        try:
            u_id = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=u_id)
        except(User.DoesNotExist, TypeError, ValueError, OverflowError):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = u_id
            messages.success(request, 'reset your password')
            return redirect('account:setpasswordview')
        else:
            messages.error(request, 'The link has been expired')
            return redirect('account:login')

class SetPasswordView(View):

    def post(self, request):
        if request.session['uid'] and not request.user.is_authenticated:
            form = SetPasswordForm(request.user, data=request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                if cleaned_data.get('new_password1') == cleaned_data.get('new_password2'):
                    user = User.objects.get(pk=request.session['uid'])
                    user.set_password(cleaned_data.get('new_password1'))
                    user.save()
                    messages.success(request, 'password reset successfully')
                    return redirect('account:login')
                else:
                    form.add_error('new_password' ,'passwords does not match')
            return render(request, 'account/change_password.html', context={'form':form})
        else:
            return redirect('account:login')

    def get(self, request):
        if request.session['uid'] and not request.user.is_authenticated:
            form = SetPasswordForm(request.user)
            return render(request, 'account/change_password.html', context={'form':form})
        else:
            return redirect('account:login')