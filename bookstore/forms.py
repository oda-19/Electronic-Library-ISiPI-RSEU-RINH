from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from bookstore.models import Book, CustomUser, Feedback, Answer, News
from django import forms




class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('foto', 'username', 'first_name', 'last_name', 'patronymic', 'birth_day', 'email',
                  'is_admin', 'is_librarian', 'is_publisher', 'password')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('foto', 'username', 'first_name', 'last_name', 'patronymic', 'birth_day', 'email',
                  'is_admin', 'is_librarian', 'is_publisher', 'password')


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'year', 'ganr', 'publisher', 'desc', 'pdf', 'cover')


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('fio', 'email', 'tema', 'message', 'userTypeF')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('fioA', 'emailA', 'temaA', 'answer', 'userTypeA')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'text', 'cover')