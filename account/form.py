from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core import validators
from account.models import User
import re

class UserCreationForm(forms.ModelForm):
    password, confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'password'}),
    ), forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'confirm-password'})
    )
    class Meta:
        model = User
        fields = ('phone',)
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password2 != password1 and password2 and password1:
            raise ValueError('passwords does not Match! ')
        return cleaned_data
    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data.get('password'))

class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'email', 'password', 'full_name', 'image', 'is_active', 'is_admin')

class PhoneValidator:
    @staticmethod
    def is_phone_start_with_09(phone: str):
        if not phone.startswith('09'):
            raise forms.ValidationError('phone should start with 09 numbers')


class RegisterForm(forms.Form):
    phone = forms.CharField(validators=(validators.MaxLengthValidator(11), PhoneValidator.is_phone_start_with_09,)
    ,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'phone number'}))

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'phone or email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(email_pattern, username):
            return username
        if username.isdigit():
            if not username.startswith('09'):
                raise ValidationError("phone should start with 09")
            if len(username) != 11:
                raise ValidationError("phone should be 11 digits")
            return username
        raise ValidationError("please enter only a valid phone number or email address")

class OtpCheckForm(forms.Form):
    code = forms.CharField(validators=(validators.MaxLengthValidator(4),),
                           widget=forms.TextInput(attrs={'placeholder':'code', 'class':'form-control'}))
    email = forms.CharField(validators=(validators.EmailValidator,),
                            widget=forms.EmailInput(attrs={'placeholder':'email', 'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password', 'class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'confirm-password', 'class':'form-control'}))

    def clean_password(self):
        password, errors, special_character = self.cleaned_data.get('password'), list(), '!@#$%^&*'
        if len(password) < 8:
            errors.append('password must be at least 8 character')
        if not any(i in special_character for i in password):
            errors.append('password must contain at least one special character')
        if not any(i.isupper() for i in password):
            errors.append('password must contain at least one uppercase letter')
        if not any(i.islower() for i in password):
            errors.append('password must contain at least one lowercase letter')
        if not any(i.isdigit() for i in password):
            errors.append('password must contain at least one number')

        if not errors:
            return password
        else:
            raise forms.ValidationError(errors)

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password and password and confirm_password:
            self.add_error('password', 'password does not match')
        else:
            return cleaned_data