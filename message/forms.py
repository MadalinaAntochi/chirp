from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# forms --> formularele scrise in python care vor aparea pe pagina web (afisarea in pagina html e facuta in views)
from message.models import Message


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

        #parola nu trebuie sa fie vizibila
        widgets = {
            "password": forms.PasswordInput(attrs={"class": "password-field"}),
        }
    retype_password=forms.CharField(widget=forms.PasswordInput)

#validarea parolelor
    def clean_retype_password (self):
        password=self.cleaned_data['password']
        retype_password=self.cleaned_data['retype_password']

        if password!=retype_password:
            raise ValidationError("The two password do not match")
        return retype_password

#salvarea datelor (in baza de date) cu parola criptata
    def save(self, commit=True):
        new_user=super(RegisterForm, self).save(commit=False)
        new_user.set_password(self.cleaned_data['password'])
        if commit:
            new_user.save()
        return  new_user


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['status']