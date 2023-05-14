from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views import View
from .models import *
from .forms import *
from django.views.generic.edit import FormView
from django.urls import reverse_lazy


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('index')
    template_name = 'login.html'

    def form_valid(self, form):
        login(self.request, form.cleaned_data['user'])
        return super().form_valid(form)


class LogoutView(View):
    def get(self,  request):
        logout(request)
        return redirect('index')


class CreateUserView(FormView):
    form_class = UserForm
    success_url = reverse_lazy('index')
    template_name = 'create_user.html'

    def form_valid(self, form):
        User.objects.create_user(
            username=form.cleaned_data['user_name'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email']
        )
        return super().form_valid(form)
