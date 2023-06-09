from django.contrib.auth import authenticate
from django import forms
from .models import *


class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=150, label='Nazwa użytkownika')
    password = forms.CharField(max_length=150, label='Hasło', widget=forms.PasswordInput())

    def clean(self):
        data = super().clean()
        u = authenticate(username=data['user_name'], password=data['password'])
        if u is None:
            raise forms.ValidationError('Nieprawidłowa nazwa użytkownika lub hasło')
        else:
            data['user'] = u
        return data


class UserForm(forms.Form):
    user_name = forms.CharField(max_length=150, label='Nazwa użytkownika')
    password = forms.CharField(max_length=150, label='Hasło', widget=forms.PasswordInput())
    password_rep = forms.CharField(max_length=150, label='Hasło ponownie', widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=150, label='Imię')
    last_name = forms.CharField(max_length=150, label='Nazwisko')
    email = forms.EmailField(label='E-mail')

    def clean(self):
        data = super().clean()
        if User.objects.filter(username=data['user_name']):
            raise forms.ValidationError('Użytkownik o podanej nazwie istnieje')
        if data['password'] != data['password_rep']:
            raise forms.ValidationError('Wprowadzone hasła nie pasują do siebie')
        return data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['sex', 'age', 'height', 'weight']


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ('title', 'description', 'trainers', 'capacity', 'start_time', 'end_time')
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'trainers': forms.CheckboxSelectMultiple,
        }


class TrainingRegistrationForm(forms.Form):
    training_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean_training_id(self):
        training_id = self.cleaned_data.get('training_id')
        try:
            training = Training.objects.get(pk=training_id)
        except Training.DoesNotExist:
            raise forms.ValidationError('Invalid training')
        return training_id


