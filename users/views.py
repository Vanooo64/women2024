from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизація'}


    # def get_success_url(self): # функція перенаправляє користувача на необхідну сторінку 'home' у разі успішної авторизації
    #     return reverse_lazy('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регістрація'}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {"title": "Профайл Користувача"}

    def get_seccess_url(self):
        """
        Повертає URL для перенаправлення після успішного оновлення профілю.
        """
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """
        Повертає поточного користувача для редагування або перегляду профілю.
        """
        return self.request.user  # Повертає об'єкт користувача, який зробив запит.


