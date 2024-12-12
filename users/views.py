from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from users.forms import LoginUserForm, RegisterUserForm


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


# def register(request): #
#     if request.method == 'POST': #якщо мметод передачі пост
#         form = RegisterUserForm(request.POST) # створюэться форма з переданними данними
#         if form.is_valid(): # чи вырно заповнены поля форми
#             user = form.save(commit=False) # формуеться обект user
#             user.set_password(form.cleaned_data['password']) # set_password - шифрування пароля, cleaned_data['password'] - занесення в атрибут класу RegisterUserForm
#             user.save() # занесення в БД
#             return render(request, 'users/register_done.html') # відображення шаблону
#     else: # якщо прийшов GET запит
#         form = RegisterUserForm() # формуэться пуста форма
#     return render(request, 'users/register.html', {'form': form}) # відображається в шаблонні регистрації
#
#
#     form = RegisterUserForm() #створюємо обїект форми регістрації
#     return render(request, 'users/register.html', {'form': form})



