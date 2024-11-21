from django.contrib import admin, messages
from .models import Women, Category

class MarriedFilter(admin.SimpleListFilter):
    title = "Статусом жінок"
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Заміжня'),
            ('single', 'Не заміжня'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'slug', 'cat', 'husband', 'tags'] #поля які выдображаються в формі для редагуванння записів
    # exclude = ['tags', 'is_published'] #виключае обранны поля з формі для редагуванння записів
    # readonly_fields = ['slug'] #поля будуть выдображатись в формы для рдагування, але редагувати їх неможна
    prepopulated_fields = {'slug': ("title", )} # автоматично формуэ слаг на основі заголовку
    filter_horizontal = ['tags'] #змінює вигляд форми редагуванння записів
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info') #відображення в адммін панелі
    list_display_links = ('title', ) #клікабельні поля в адмінке
    ordering = ['time_create', 'title'] #сортування в адмінке
    list_editable = ('is_published',  ) # поля які можна редагувати
    list_per_page = 5 #пагінація статей (максимальна кількість яка відображається на адмін панелі
    actions = ['set_published', 'set_draft'] #список додавання дій
    search_fields = ['title', 'cat__name'] # панель пошуку
    list_filter = [MarriedFilter, 'cat__name', 'is_published'] # панель з фільтами

    @admin.display(description='Короткий опис', ordering='content')
    def brief_info(self, women: Women): #визначає кількість символів в описі
        return f"Опис {len(women.content)} символів"

    @admin.action(description='Опублікувати обранні записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Змінено {count} записи")


    @admin.action(description='Зняти з публікації')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"{count} записи знято з публікації", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') #відображення в адммін панелі
    list_display_links = ('id', 'name') #клікабельні поля в адмінке




