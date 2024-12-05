from django.contrib import admin, messages
from django.utils.safestring import mark_safe

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
    fields = ['title', 'content', 'slug', 'photo', 'post_photo', 'cat', 'husband', 'tags'] #поля які відображаються в формі для редагуванння записів
    # exclude = ['tags', 'is_published'] #виключае обранны поля з формі для редагуванння записів
    readonly_fields = ['post_photo'] #поля будуть відображатись в формі для рдагування, але редагувати їх неможна
    prepopulated_fields = {'slug': ("title", )} # автоматично формуэ слаг на основі заголовку
    # filter_horizontal = ['tags'] #змінює вигляд форми редагуванння записів
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat') #відображення в адммін панелі
    list_display_links = ('title', ) #клікабельні поля в адмінке
    ordering = ['time_create', 'title'] #сортування в адмінке
    list_editable = ('is_published',  ) # поля які можна редагувати
    list_per_page = 5 #пагінація статей (максимальна кількість яка відображається на адмін панелі
    actions = ['set_published', 'set_draft'] #список додавання дій
    search_fields = ['title', 'cat__name'] # панель пошуку
    list_filter = [MarriedFilter, 'cat__name', 'is_published'] # панель з фільтами
    save_on_top = True #панель для зберігання запису буде відображуватись з верху форми редагування

    # @admin.display(description='Короткий опис', ordering='content')
    # def brief_info(self, women: Women): #визначає кількість символів в описі
    #     return f"Опис {len(women.content)} символів"

    @admin.display(description='Зображення', ordering='content')
    def post_photo(self, women: Women): #функція повертає HTML фрагмент з фото
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50") #функція mark_safe того щоб HTML теги нне екранувалися
        return 'Відсутне'

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




