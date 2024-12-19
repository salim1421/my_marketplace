from django.shortcuts import redirect, render
from django.views.generic import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User, auth


from .forms import UserRegForm


class RegisterView(FormView):
    model = User
    form_class = UserRegForm
    success_url = 'login'

    def form_valid(self, form):
        user = form.save()
        if form.is_valid:
            auth.login(self.request, user)
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return self.get(request, *args, **kwargs)
    

