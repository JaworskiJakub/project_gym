"""
URL configuration for gym project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gym_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add_user/', CreateUserView.as_view(), name='add_user'),
    path('profile/', update_profile, name='update_profile'),
    path('profile_info/', profile_info, name='profile_info'),
    path('add_training/', TrainingAddView.as_view(), name='add_training'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('calendar/training/<int:id>/', TrainingView.as_view(), name='training_details'),
    path('purchase/', PurchaseMembership.as_view(), name='purchase_membership'),
    path('purchase_success/', membership_success, name='membership_success'),
    path('membership_history/', membership_history, name='membership_history')
]
