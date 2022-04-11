from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic as generic_views

from DesertTraders.users.forms import CustomUserRegisterForm, CustomUserLoginForm


class UserRegistrationView(generic_views.CreateView):
    template_name = 'users/user_auth/register.html'
    form_class = CustomUserRegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form ):
        result = super().form_valid(form)

        login(self.request, self.object)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'users/user_auth/login.html'
    form_class = CustomUserLoginForm

    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(auth_views.LogoutView):
    def get_next_page(self):
        return reverse_lazy('home')

