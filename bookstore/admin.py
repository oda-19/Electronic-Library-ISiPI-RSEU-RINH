from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book, Feedback, Answer, News


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = []
    model = CustomUser

    list_display = ['username', 'last_name', 'first_name', 'patronymic', 'birth_day', 'email',
                  'is_superuser', 'is_admin', 'is_librarian', 'is_publisher']
    search_fields = ['username', 'last_name', 'first_name', 'patronymic', 'birth_day', 'email']
    list_filter = ['last_name']
    list_editable = ['last_name', 'first_name', 'patronymic', 'birth_day', 'email']
    readonly_fields = ('date_joined', 'last_login')

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'patronymic',
                    'birth_day',
                    'is_admin',
                    'is_librarian',
                    'is_publisher',
                    'foto',
                )
            }
        )
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'patronymic',
                    'birth_day',
                    'is_admin',
                    'is_librarian',
                    'is_publisher',
                    'foto',
                )
            }
        )
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'year', 'ganr', 'publisher']
    search_fields = ['title', 'author', 'year', 'ganr', 'publisher']
    list_filter = ['year', 'ganr', 'publisher']
    list_editable = ['author', 'year', 'ganr', 'publisher']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['fio', 'email', 'tema']
    search_fields = ['fio', 'email', 'tema']
    list_filter = ['tema']
    list_editable = ['tema']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['fioA', 'emailA', 'temaA']
    search_fields = ['fioA', 'emailA', 'temaA']
    list_filter = ['temaA']
    list_editable = ['temaA']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_filter = ['title']

