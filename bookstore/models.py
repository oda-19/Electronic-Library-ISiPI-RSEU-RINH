from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.models import User




class CustomUser(AbstractUser):
    foto = models.ImageField('Аватар', upload_to='bookapp/fotos/', null=True, default='/bookapp/fotos/Avatar.jpg')
    patronymic = models.CharField('Отчество', max_length=150, default='')
    birth_day = models.DateField('Дата рождения', default='2000-01-01')
    is_admin = models.BooleanField('Администратор', default=False)
    is_publisher = models.BooleanField('Студент', default=False)
    is_librarian = models.BooleanField('Преподаватель', default=False)


    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Book(models.Model):
    title = models.CharField('Название', max_length=100)
    author = models.CharField('Автор', max_length=100)
    year = models.IntegerField('Год', max_length=4)
    ganr = models.CharField('Жанр', max_length=100)
    publisher = models.CharField('Издательство', max_length=200)
    desc = models.TextField('Аннотация', max_length=1000)
    pdf = models.FileField('PDF', upload_to='bookapp/pdfs/')
    cover = models.ImageField('Обложка', upload_to='bookapp/covers/')
    uploaded_by = models.CharField('Добавил пользователь', max_length=100)
    user_id = models.CharField('ID пользователя', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)        


class Feedback(models.Model):
    Registration = 'Регистрация'
    Authorization = 'Авторизация'
    Books = 'Книги'
    Users = 'Пользователи'
    News = 'Новости'
    Other = 'Другое'

    TEMA_CHOICES = (
        (Registration, 'Регистрация'),
        (Authorization, 'Авторизация'),
        (Books, 'Книги'),
        (Users, 'Пользователи'),
        (News, 'Новости'),
        (Other, 'Другое'),
    )

    Admin = 'Администратор'
    Publisher = 'Студент'
    Librarian = 'Преподаватель'

    USERTYPE_CHOICES = (
        (Admin, 'Администратор'),
        (Publisher, 'Студент'),
        (Librarian, 'Преподаватель'),
    )

    user_id = models.CharField('ID пользователя', max_length=100, null=True, blank=True)
    uploaded_by = models.CharField('Отправил пользователь', max_length=100)
    fio = models.CharField('ФИО', max_length=254)
    email = models.EmailField(blank=True, max_length=254)
    tema = models.CharField('Тема', max_length=12, choices=TEMA_CHOICES)
    userTypeF = models.CharField('Роль', max_length=13, choices=TEMA_CHOICES)
    message = models.TextField(max_length=400, blank=True)


    def __str__(self):
        return self.message


class Answer(models.Model):
    fioA = models.CharField('ФИО', max_length=254)
    emailA = models.EmailField(blank=True, max_length=254)
    temaA = models.CharField('Тема', max_length=12)
    userTypeA = models.CharField('Роль', max_length=20)
    answer = models.TextField(max_length=400, blank=True)


    def __str__(self):
        return self.answer


class News(models.Model):
    title = models.CharField('Название', max_length=100)
    text = models.TextField('Текст публикации', max_length=1000)
    cover = models.ImageField('Обложка', upload_to='bookapp/public/')
    uploaded_by = models.CharField('Добавил пользователь', max_length=100)
    user_id = models.CharField('ID пользователя', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title