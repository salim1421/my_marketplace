from django.shortcuts import redirect, render
from django.views.generic import FormView, UpdateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import PasswordChangeForm


from .forms import UserRegForm, UserChangeViewForm


class RegisterView(FormView):
    model = User
    form_class = UserRegForm
    template_name = 'users/register.html'
    success_url = 'login'

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            auth.login(self.request, user)
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().get(request, *args, **kwargs)
    

class SignInView(LoginView):
    success_url = '/'
    redirect_authenticated_user = True
    template_name = 'users/login.html'


def logout(request):
    auth.logout(request)
    return redirect('/')


class UserInfoChangeView(UpdateView):
    model = User
    template_name = 'users/user_settings.html'
    form_class = UserChangeViewForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_form.html'
    form_class = PasswordChangeForm
    success_url = 'login'

