from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін',
                    widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логін')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model() #повертає поточну модель користувача
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2'] #  поля які відображаються в формі
        labels = {
            'email': 'E-mail',
            'first_name': 'Ім`я',
            'last_name': 'Фамілія',
        }

    def clean_password2(self): #перевірка співпадіння паролів
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Паролі не співападають')
        return cd['password']

    def clean_email(self):
        """
        Метод для перевірки унікальності електронної пошти в формі.

        1. Отримує введене значення поля 'email' з очищених даних форми.
        2. Перевіряє, чи існує вже запис у базі даних з таким значенням email:
           - get_user_model(): отримує модель користувача, яка використовується в проєкті
             (стандартна User або кастомна, вказана в AUTH_USER_MODEL).
           - .filter(email=email): формує запит до бази даних, щоб знайти всі записи,
             у яких поле 'email' співпадає з введеним значенням.
           - .exists(): перевіряє, чи є хоча б один запис, який відповідає критерію запиту.
        3. Якщо такий email уже є в базі даних, піднімається ValidationError із відповідним повідомленням.
        4. Якщо перевірка пройшла успішно, повертається очищене значення email.
        """
        email = self.cleaned_data['email']  # Отримуємо значення поля 'email' з очищених даних форми.
        if get_user_model().objects.filter(email=email).exists():  # Перевіряємо, чи існує запис із таким email.
            raise forms.ValidationError('Такий E-mail вже існує')  # Якщо запис знайдено, піднімаємо помилку.
        return email  # Повертаємо очищене значення email, якщо воно унікальне.

