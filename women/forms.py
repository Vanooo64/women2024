from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible


from .models import Category, Husband

@deconstructible
class UkraineValidator:
    ALLOWED_CHARS = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзииіїйклмнопрстуфхцчшщьюя0123456789- '
    code = 'ukraine'

    def __init__(self, message=None):
        self.message = message if message else 'Повинен містити тільки українскі символи, дефіз і пробіл.'

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)
#

class AddPostForm(forms.Form): # створюється при багаторазовій перевірці
    title = forms.CharField(max_length=255, min_length=5,
                            label='Заголовок',
                            widget=forms.TextInput(attrs={'class': 'form-input'}),
                            validators=[
                                UkraineValidator(),
                            ],
                            error_messages={
                                'min_length': 'Дуже короткий заголовок',
                                'required': 'Без заголовку ніяк!!!',
                            })
    slug = forms.SlugField(max_length=255, label='URL',
                           validators=[
                               MinLengthValidator(5, message='Ведіть мінімум 5 символів'),
                               MaxLengthValidator(100, message='Максимум 100 символів'),
                           ])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент')
    is_published = forms.BooleanField(required=False, initial=True, label='Статус')
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категорія не обрана', label='Категорії')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label='Немає чоловіка', label='Чоловік')

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     ALLOWED_CHARS = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзииіїйклмнопрстуфхцчшщьюя0123456789- '
    #
    #     if not (set(title) <= set(ALLOWED_CHARS)):
    #         raise ValidationError('Повинен містити тільки українскі символи, дефіз і пробіл.')

