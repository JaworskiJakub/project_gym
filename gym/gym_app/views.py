from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views import View, generic
from .models import *
from .forms import *
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from .utils import Calendar
from datetime import datetime, timedelta, date
from django.utils.safestring import mark_safe
import calendar
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import datetime


class IndexView(View):
    """Returns the index view of the application."""

    def get(self, request):
        return render(request, 'index.html')


class LoginView(FormView):
    """Enables the user to login. If the login is successful, the uer is redirected to index page."""

    form_class = LoginForm
    success_url = reverse_lazy('index')
    template_name = 'login.html'

    def form_valid(self, form):
        login(self.request, form.cleaned_data['user'])
        return super().form_valid(form)


class LogoutView(View):
    """Enables the user to logout."""

    def get(self,  request):
        logout(request)
        return redirect('index')


class CreateUserView(FormView):
    """A class used to let  the user create an account. If the account creation is successful,
     user is redirected to login page. """

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
    """Requires the user to be logged in. Enables user to set additional information about his profile."""

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
    """Requires the user to be logged in. Return the user profile information."""

    if request.method == 'GET':
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        ctx = {
            'user': user
        }
        return render(request, 'profile_info.html', ctx)


class TrainingAddView(PermissionRequiredMixin, View):
    """The user needs to have the 'add_training' permission to access this view.
    The class provides the form to create new training."""

    permission_required = ('gym_app.add_training',)

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
    """Returns the calendar of the current month with the trainings that are planned.
     Enables user to check next  or previous months."""

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
        return date.today()


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


class TrainingView(View):
    """Returns the page with training details. Training ID has to be given in the URL."""

    def get(self, request, id):
        training = Training.objects.get(pk=id)
        ctx = {
            'training': training
        }
        return render(request, 'training_details.html', ctx)


class PurchaseMembership(LoginRequiredMixin, View):
    """Login is required for this view. The class allows the user to choose the membership option,
     checks what is the actual user membership status and extend the actual membership by chosen duration or start
     new membership from actual date."""

    login_url = "login"
    redirect_field_name = "purchase_membership"

    def get(self, request):
        memberships = Membership.objects.all()
        return render(request, 'purchase_membership.html', {'memberships': memberships})

    def post(self, request):
        user_profile, created = UserMembership.objects.get_or_create(user=request.user)
        selected_membership_id = request.POST.get('membership')
        selected_membership = Membership.objects.get(pk=selected_membership_id)
        user_profile.membership = selected_membership
        if user_profile.expiration_date and user_profile.expiration_date > timezone.now().date():
            user_profile.expiration_date += timezone.timedelta(days=selected_membership.duration)
        else:
            user_profile.expiration_date = timezone.now().date() + timezone.timedelta(
                days=selected_membership.duration)
        user_profile.save()
        MembershipHistory.objects.create(user_membership=user_profile, membership=selected_membership)
        return redirect('membership_success')


@login_required
def membership_success(request):
    """Login is required. Shows the actual membership information."""

    user_profile = UserMembership.objects.get(user=request.user)
    return render(request, 'membership_success.html', {'user_profile': user_profile})


@login_required
def membership_info(request):
    """Shows the actual membership expiration date and the membership purchase history."""

    try:
        user_profile = UserMembership.objects.get(user=request.user)
    except UserMembership.DoesNotExist:
        return HttpResponse('Membership does not exist.')
    history = MembershipHistory.objects.filter(user_membership__user=request.user).order_by('-purchase_date')
    ctx = {
        'user_profile': user_profile,
        'history': history
    }
    return render(request, 'membership_info.html', ctx)


@permission_required('gym_app.view_membershiphistory')
def membership_history(request):
    """Requires 'view_membershiphistory' permission. Returns whole membership history. Allows user to filter
    the history by purchase date."""

    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        history = MembershipHistory.objects.filter(purchase_date=selected_date)
    else:
        history = MembershipHistory.objects.all()

    return render(request, 'membership_history.html', {'history': history})


class TrainingRegisterView(LoginRequiredMixin, View):
    """Login is required. Can be accessed through calendar view. Allows the user to enroll for the training.
    Checks if the user has active membership and if the user is already enrolled. Discounts training free spots."""

    login_url = "login"

    def get(self, request, id):
        training = get_object_or_404(Training, pk=id)
        initial_data = {
            'training_id': id,
        }
        form = TrainingRegistrationForm(initial=initial_data)
        return render(request, 'training_register.html', {'form': form, 'training': training})

    def post(self, request, id):
        form = TrainingRegistrationForm(request.POST)
        training = get_object_or_404(Training, pk=id)

        has_active_membership = UserMembership.objects.filter(user=request.user,
                                                              expiration_date__gte=timezone.now().date()).exists()
        if not has_active_membership:
            return redirect('purchase_membership')

        is_registered = training.registered_users.filter(id=request.user.id).exists()
        if is_registered:
            return HttpResponse('You are already enrolled!')

        if form.is_valid():
            user = request.user
            training.registered_users.add(user)
            if training.capacity > 0:
                training.capacity -= 1
                training.save()
            else:
                HttpResponse('Training is full!')
            return redirect('index')
        else:
            return render(request, 'training_register.html', {'form': form, 'training': training})

