from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views import View, generic
from .models import *
from .forms import *
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .utils import Calendar
from datetime import datetime, timedelta, date
from django.utils.safestring import mark_safe
import calendar


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
    success_url = reverse_lazy('login')
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


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('index')
        else:
            profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'profile.html', {
            'profile_form': profile_form
        })
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'profile_form': profile_form
    })


@login_required
def profile_info(request):
    if request.method == 'GET':
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        ctx = {
            'user': user
        }
        return render(request, 'profile_info.html', ctx)


class TrainingAddView(View):
    def get(self, request):
        form = TrainingForm()
        ctx = {
            'form': form
        }
        return render(request, 'add_training.html', ctx)

    def post(self, request):
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        ctx = {
            'form': form
        }
        return render(request, 'add_training.html', ctx)


class CalendarView(generic.ListView):
    model = Training
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        d = get_date(self.request.GET.get('month', None))

        cal = Calendar(d.year, d.month)

        html_cal = cal.formatmonth(withyear=True)

        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    else:
        return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
