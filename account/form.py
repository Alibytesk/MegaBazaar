from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from account.models import User

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
