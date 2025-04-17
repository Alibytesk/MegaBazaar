from django import forms
from account.models import Address, User

class AddressSelectionForm(forms.Form):
    address = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['address'].queryset = Address.objects.filter(user=user)

class OrderProfileForm(forms.ModelForm):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'})
    )
    def __init__(self, *args, **kwargs):
        super(OrderProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone'].disabled = True

    class Meta:
        model = User
        fields = ('phone',)

