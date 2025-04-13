from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, SetPasswordMixin
from django.core.exceptions import ValidationError
from django.core import validators
from account.models import User
from account import validation
import re

class UserUpdateForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Phone')
    email = forms.CharField(
        validators=(validators.EmailValidator,),
        widget=forms.EmailInput(attrs={'class':'form-control'}),
        label='Email Address'
    )
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'form-control'}), label='image', required=False)
    full_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class':'form-control'}), label='full_name', required=False)

    class Meta:
        model = User
        fields = ('phone', 'email', 'full_name', 'image')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['phone'].disabled = True
        self.fields['email'].disabled = True

class EmailVerifyForm(forms.ModelForm):
    email = forms.CharField(
        validators=(validators.EmailValidator,),
        widget=forms.EmailInput(attrs={'class':'form-control'}),
        label='Email Address'
    )
    code = forms.CharField(validators=(validators.MaxLengthValidator(6),),
                           widget=forms.NumberInput(attrs={'placeholder':'code', 'class':'form-control'}),
                           label='code')
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(EmailVerifyForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True

class UserCreationForm(forms.ModelForm):
    password, confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'password'}),
    ), forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'confirm-password'})
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





class RegisterForm(forms.Form):
    phone = forms.CharField(validators=(validators.MaxLengthValidator(11), validation.PhoneValidator.is_phone_start_with_09,)
                            , widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone number'}))


class OtpCheckForm(forms.Form):
    code = forms.CharField(validators=(validators.MaxLengthValidator(4),),
                           widget=forms.TextInput(attrs={'placeholder': 'code', 'class': 'form-control'}))
    email = forms.CharField(validators=(validators.EmailValidator,),
                            widget=forms.EmailInput(attrs={'placeholder': 'email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'confirm-password', 'class': 'form-control'}))

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validation.PasswordValidation.password_validation(password)

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password and password and confirm_password:
            self.add_error('password', 'password does not match')
        else:
            return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone or email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))

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

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'current-password', 'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'new-password', 'class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'confirm-password', 'class':'form-control'}))

    def clean_password1(self):
        validation.PasswordValidation.password_validation(self.cleaned_data.get('password1'))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password1 != confirm_password and password1 and confirm_password:
            raise forms.ValidationError('password does not Match! ')
        else:
            return password1

class ForgotPasswordForm(forms.Form):
    email = forms.CharField(validators=(validators.EmailValidator,)
            ,widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'enter your email'}))

class SetPasswordForm(SetPasswordMixin, forms.Form):
    new_password1, new_password2 = SetPasswordMixin.create_password_fields(
        label1="New password", label2="New password confirmation"
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        self.validate_passwords("new_password1", "new_password2")
        self.validate_password_for_user(self.user, "new_password2")
        return super().clean()

    def save(self, commit=True):
        return self.set_password_and_save(self.user, "new_password1", commit=commit)
