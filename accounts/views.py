from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "accounts/login.html"


class SignUpView(CreateView):
    template_name = "accounts/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("index")