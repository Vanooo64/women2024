from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import LoginUserForm


def login_user(request): #HTTP-запит, який надходить від користувача (GET або POST).
    if request.method == 'POST': #якщо метод передачі форми = POST
        form = LoginUserForm(request.POST) #заповнюємо форму данними які були передані на сервер
        if form.is_valid(): # перевіряємо коректність заповнення полів
            cd = form.cleaned_data #зявляється колекція cleaned_data
            user = authenticate(request, username=cd['username'], #за допомогою функції authenticate перевіряється, чи існує користувач із зазначеним логіном (username) і паролем (password)
                                password=cd['password'])
            if user and user.is_active: #Якщо користувач є валідним (user) і його обліковий запис активний (user.is_active), то функція login виконує вхід користувача в систему
                login(request, user) #дозволяє користувачу нелогінинтись при повторному вході
                return HttpResponseRedirect(reverse('home')) #перенаправлення на домашню сторінку:
    else:
        form = LoginUserForm() # Якщо метод запиту не POST, створюється порожня форма для входу
    return render(request, 'users/login.html', {'form': form}) #повертає HTML-сторінку users/login.html з контекстом, що містить форму form.


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))
