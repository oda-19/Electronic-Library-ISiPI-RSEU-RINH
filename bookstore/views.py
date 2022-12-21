from django.core.mail import EmailMultiAlternatives
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import get_template
from django.urls import reverse_lazy
from .models import CustomUser, Book, Feedback, Answer, News
from django.views.generic import DetailView, DeleteView, UpdateView, ListView
from .forms import BookForm, FeedbackForm
from . import models
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required




# Общие
def main(request):
    return render(request, 'bookstore/main.html')


def login_form(request):
    return render(request, 'bookstore/login.html')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            elif user.is_librarian:
                return redirect('librarian')
            else:
                return redirect('publisher')
        else:
            messages.info(request, "Неправильный логин или пароль!")
            return redirect('login_form')


def logoutView(request):
    logout(request)
    return redirect('home')


def register_form(request):
    choice = ['1', '0', 'Студент', 'Преподаватель']
    choice = {'choice': choice}
    return render(request, 'bookstore/register.html', choice)


def registerView(request):
    choice = ['1', '0', 'Студент', 'Преподаватель']
    choice = {'choice': choice}

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        patronymic = request.POST['patronymic']
        birth_day = request.POST['birth_day']
        userType = request.POST['userType']
        foto = request.FILES['foto']
        password = request.POST['password']
        password = make_password(password)

        if userType == "Студент":
            a = CustomUser(username=username, email=email, last_name=last_name, first_name=first_name,
                           patronymic=patronymic, birth_day=birth_day, is_publisher=True, foto=foto, password=password)

            if CustomUser.objects.filter(username=username).exists():
                messages.success(request, 'Пользователь с таким логином уже существует')
                return redirect('login_form')
            else:
                a.save()
                messages.success(request, 'Аккаунт успешно создан')
                return redirect('login_form')

        elif userType == "Преподаватель":
            a = CustomUser(username=username, email=email, last_name=last_name, first_name=first_name,
                           patronymic=patronymic, birth_day=birth_day, is_librarian=True, foto=foto, password=password)

            if CustomUser.objects.filter(username=username).exists():
                messages.success(request, 'Пользователь с таким логином уже существует')
                return redirect('login_form')
            else:
                a.save()
                messages.success(request, 'Аккаунт успешно создан')
                return redirect('login_form')

        else:
            messages.error(request, 'Ошибка, попробуйте позже')
            return redirect('regform')

    else:
        return redirect('regform')


class UBookListView(ListView):
    model = Book
    template_name = 'bookstore/allbooks.html'
    context_object_name = 'books'
    paginate_by = 8


    def get_queryset(self):
        return Book.objects.order_by('-id')


class UViewBook(DetailView):
    model = Book
    template_name = 'bookstore/detailbook.html'


def feedback_form(request):
    return render(request, 'bookstore/support.html')


def send_feedback(request):
    if request.method == 'POST':
        fio = request.POST['fio']
        email = request.POST['email']
        tema = request.POST.get('tema', False)
        message = request.POST['message']
        userTypeF = request.POST['userTypeF']

        if request.user.is_authenticated:
            current_user = request.user
            user_id = current_user.id
            username = current_user.username

            a = Feedback(fio=fio, email=email, tema=tema, message=message, userTypeF=userTypeF,
                             uploaded_by=username, user_id=user_id)
            a.save()
            messages.success(request, 'Обращение успешно отправлено')

            return redirect('feedback_form')
        else:
            a = Feedback(fio=fio, email=email, tema=tema, message=message, userTypeF=userTypeF)
            a.save()
            messages.success(request, 'Обращение успешно отправлено')
            return redirect('feedback_form')
    else:
        messages.error(request, 'Произошла ошибка, попробуйте позже')
        return redirect('feedback_form')


class NewsListView(ListView):
    model = News
    template_name = 'bookstore/allnews.html'
    context_object_name = 'news'
    paginate_by = 4


    def get_queryset(self):
        return News.objects.order_by('-id')


class AViewNews(DetailView):
    model = News
    template_name = 'bookstore/detailnews.html'


def about(request):
    return render(request, 'bookstore/about.html')


def usearch(request):
    query = request.GET['query']
    print(type(query))

    data = query
    print(len(data))
    if (len(data) == 0):
        return redirect('publisher')
    else:
        a = data

        qs1 = models.Book.objects.filter(title__iexact=a).distinct()
        qs2 = models.Book.objects.filter(title__iexact=a).distinct()
        qs3 = models.Book.objects.all().filter(title__contains=a)
        qs4 = models.Book.objects.select_related().filter(title__contains=a).distinct()
        qs5 = models.Book.objects.filter(title__startswith=a).distinct()
        qs6 = models.Book.objects.filter(title__endswith=a).distinct()
        qs7 = models.Book.objects.filter(title__istartswith=a).distinct()
        qs8 = models.Book.objects.all().filter(title__icontains=a)
        qs9 = models.Book.objects.filter(title__iendswith=a).distinct()

        qs10 = models.Book.objects.filter(author__iexact=a).distinct()
        qs11 = models.Book.objects.filter(author__iexact=a).distinct()
        qs12 = models.Book.objects.all().filter(author__contains=a)
        qs13 = models.Book.objects.select_related().filter(author__contains=a).distinct()
        qs14 = models.Book.objects.filter(author__startswith=a).distinct()
        qs15 = models.Book.objects.filter(author__endswith=a).distinct()
        qs16 = models.Book.objects.filter(author__istartswith=a).distinct()
        qs17 = models.Book.objects.all().filter(author__icontains=a)
        qs18 = models.Book.objects.filter(author__iendswith=a).distinct()

        qs19 = models.Book.objects.filter(year__iexact=a).distinct()
        qs20 = models.Book.objects.filter(year__iexact=a).distinct()
        qs21 = models.Book.objects.all().filter(year__contains=a)
        qs22 = models.Book.objects.select_related().filter(year__contains=a).distinct()
        qs23 = models.Book.objects.filter(year__startswith=a).distinct()
        qs24 = models.Book.objects.filter(year__endswith=a).distinct()
        qs25 = models.Book.objects.filter(year__istartswith=a).distinct()
        qs26 = models.Book.objects.all().filter(year__icontains=a)
        qs27 = models.Book.objects.filter(year__iendswith=a).distinct()

        qs28 = models.Book.objects.filter(publisher__iexact=a).distinct()
        qs29 = models.Book.objects.filter(publisher__iexact=a).distinct()
        qs30 = models.Book.objects.all().filter(publisher__contains=a)
        qs31 = models.Book.objects.select_related().filter(publisher__contains=a).distinct()
        qs32 = models.Book.objects.filter(publisher__startswith=a).distinct()
        qs33 = models.Book.objects.filter(publisher__endswith=a).distinct()
        qs34 = models.Book.objects.filter(publisher__istartswith=a).distinct()
        qs35 = models.Book.objects.all().filter(publisher__icontains=a)
        qs36 = models.Book.objects.filter(publisher__iendswith=a).distinct()

        files = itertools.chain(qs1, qs2, qs3, qs4, qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13, qs14, qs15, qs16,
                                qs17, qs18, qs19, qs20, qs21, qs22, qs23, qs24, qs25, qs26, qs27, qs28, qs29, qs30, qs31,
                                qs32, qs33, qs34, qs35, qs36)

        res = []
        for i in files:
            if i not in res:
                res.append(i)

        print(res)
        files = res

        page = request.GET.get('page', 1)
        paginator = Paginator(files, 12)
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)

        if files:
            return render(request, 'bookstore/searchresult.html', {'files': files})
        return render(request, 'bookstore/searchresult.html', {'files': files})




# Студент
class ALViewUser(DetailView):
    model = CustomUser
    template_name = 'publisher/detailuser.html'




# Преподаватель
class LBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'librarian/allbooks.html'
    context_object_name = 'books'
    paginate_by = 8

    def get_queryset(self):
        return Book.objects.order_by('-id')


@login_required
def labook_form(request):
    choice = ['Прикладная и научно-популярная литература', 'Универсально-справочная литература', 'Художественная литература',
              'Журналы', 'Учебно-методическая литература', 'Учебные пособия', 'Монография']
    choice = {'choice': choice}
    return render(request, 'librarian/addbook.html', choice)


@login_required
def labook(request):
    choice = ['Прикладная и научно-популярная литература', 'Универсально-справочная литература', 'Художественная литература',
              'Журналы', 'Учебно-методическая литература', 'Учебные пособия', 'Монография']
    choice = {'choice': choice}

    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        publisher = request.POST['publisher']
        year = request.POST['year']
        ganr = request.POST['ganr']
        desc = request.POST['desc']
        cover = request.FILES['cover']
        pdf = request.FILES['pdf']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        a = Book(title=title, author=author, publisher=publisher, year=year, ganr=ganr, desc=desc, cover=cover, pdf=pdf,
                 uploaded_by=username, user_id=user_id)
        a.save()
        messages.success(request, 'Книга успешно добавлена')
        return redirect('librarian')
    else:
        messages.error(request, 'Произошла ошибка, попробуйте позже')
        return redirect('labook_form')


@login_required
def lsearch(request):
    query = request.GET['query']
    print(type(query))

    data = query
    print(len(data))
    if (len(data) == 0):
        return redirect('librarian')
    else:
        a = data

        qs1 = models.Book.objects.filter(title__iexact=a).distinct()
        qs2 = models.Book.objects.filter(title__iexact=a).distinct()
        qs3 = models.Book.objects.all().filter(title__contains=a)
        qs4 = models.Book.objects.select_related().filter(title__contains=a).distinct()
        qs5 = models.Book.objects.filter(title__startswith=a).distinct()
        qs6 = models.Book.objects.filter(title__endswith=a).distinct()
        qs7 = models.Book.objects.filter(title__istartswith=a).distinct()
        qs8 = models.Book.objects.all().filter(title__icontains=a)
        qs9 = models.Book.objects.filter(title__iendswith=a).distinct()

        qs10 = models.Book.objects.filter(author__iexact=a).distinct()
        qs11 = models.Book.objects.filter(author__iexact=a).distinct()
        qs12 = models.Book.objects.all().filter(author__contains=a)
        qs13 = models.Book.objects.select_related().filter(author__contains=a).distinct()
        qs14 = models.Book.objects.filter(author__startswith=a).distinct()
        qs15 = models.Book.objects.filter(author__endswith=a).distinct()
        qs16 = models.Book.objects.filter(author__istartswith=a).distinct()
        qs17 = models.Book.objects.all().filter(author__icontains=a)
        qs18 = models.Book.objects.filter(author__iendswith=a).distinct()

        qs19 = models.Book.objects.filter(year__iexact=a).distinct()
        qs20 = models.Book.objects.filter(year__iexact=a).distinct()
        qs21 = models.Book.objects.all().filter(year__contains=a)
        qs22 = models.Book.objects.select_related().filter(year__contains=a).distinct()
        qs23 = models.Book.objects.filter(year__startswith=a).distinct()
        qs24 = models.Book.objects.filter(year__endswith=a).distinct()
        qs25 = models.Book.objects.filter(year__istartswith=a).distinct()
        qs26 = models.Book.objects.all().filter(year__icontains=a)
        qs27 = models.Book.objects.filter(year__iendswith=a).distinct()

        qs28 = models.Book.objects.filter(publisher__iexact=a).distinct()
        qs29 = models.Book.objects.filter(publisher__iexact=a).distinct()
        qs30 = models.Book.objects.all().filter(publisher__contains=a)
        qs31 = models.Book.objects.select_related().filter(publisher__contains=a).distinct()
        qs32 = models.Book.objects.filter(publisher__startswith=a).distinct()
        qs33 = models.Book.objects.filter(publisher__endswith=a).distinct()
        qs34 = models.Book.objects.filter(publisher__istartswith=a).distinct()
        qs35 = models.Book.objects.all().filter(publisher__icontains=a)
        qs36 = models.Book.objects.filter(publisher__iendswith=a).distinct()

        files = itertools.chain(qs1, qs2, qs3, qs4, qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13, qs14, qs15, qs16,
                                qs17, qs18, qs19, qs20, qs21, qs22, qs23, qs24, qs25, qs26, qs27, qs28, qs29, qs30, qs31,
                                qs32, qs33, qs34, qs35, qs36)

        res = []
        for i in files:
            if i not in res:
                res.append(i)

        print(res)
        files = res

        page = request.GET.get('page', 1)
        paginator = Paginator(files, 12)
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)

        if files:
            return render(request, 'librarian/searchresult.html', {'files': files})
        return render(request, 'librarian/searchresult.html', {'files': files})




# Администратор
@login_required
def amain(request):
    return render(request, 'dashboard/main.html')


class ALViewUserAdmin(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'dashboard/detailuser.html'


class ABookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'dashboard/allbooks.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.order_by('-id')


class AViewBook(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'dashboard/detailbook.html'


class AEditView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'dashboard/editbook.html'
    success_url = reverse_lazy('dashboard')
    success_message = 'Книга успешно отредактирована'


class ADeleteBook(SuccessMessageMixin, DeleteView):
    model = Book
    template_name = 'dashboard/deletebook.html'
    success_url = reverse_lazy('dashboard')
    success_message = 'Книга успешно удалена'


@login_required
def aabook_form(request):
    choice = ['Прикладная и научно-популярная литература', 'Универсально-справочная литература', 'Художественная литература',
              'Журналы', 'Учебно-методическая литература', 'Учебные пособия', 'Монография']
    choice = {'choice': choice}
    return render(request, 'dashboard/addbook.html', choice)


@login_required
def aabook(request):
    choice = ['Прикладная и научно-популярная литература', 'Универсально-справочная литература', 'Художественная литература',
              'Журналы', 'Учебно-методическая литература', 'Учебные пособия', 'Монография']
    choice = {'choice': choice}

    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        publisher = request.POST['publisher']
        year = request.POST['year']
        ganr = request.POST['ganr']
        desc = request.POST['desc']
        cover = request.FILES['cover']
        pdf = request.FILES['pdf']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        a = Book(title=title, author=author, publisher=publisher, year=year, ganr=ganr, desc=desc, cover=cover, pdf=pdf,
                 uploaded_by=username, user_id=user_id)
        a.save()
        messages.success(request, 'Книга успешно добавлена')

        return redirect('dashboard')
    else:
        messages.error(request, 'Произошла ошибка, попробуйте позже')
        return redirect('aabook_form')


class ListUserView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'dashboard/allusers.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        return CustomUser.objects.order_by('-id')


class ADeleteUser(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'dashboard/deleteuser.html'
    success_url = reverse_lazy('aluser')
    success_message = 'Пользователь успешно удален'


@login_required
def user_form(request):
    choice = ['1', '0', 'Администратор', 'Студент', 'Преподаватель']
    choice = {'choice': choice}
    return render(request, 'dashboard/adduser.html', choice)


@login_required
def userView(request):
    choice = ['1', '0', 'Администратор', 'Студент', 'Преподаватель']
    choice = {'choice': choice}

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        patronymic = request.POST['patronymic']
        birth_day = request.POST['birth_day']
        userType = request.POST['userType']
        foto = request.FILES['foto']
        password = request.POST['password']
        password = make_password(password)

        if userType == "Администратор":
            a = CustomUser(username=username, email=email, last_name=last_name, first_name=first_name,
                           patronymic=patronymic, birth_day=birth_day, is_admin=True, foto=foto, password=password)

            if CustomUser.objects.filter(username=username).exists():
                messages.success(request, 'Пользователь с таким логином уже существует')
                return redirect('aluser')
            else:
                a.save()
                messages.success(request, 'Аккаунт успешно создан')
                return redirect('aluser')

        elif userType == "Студент":
            a = CustomUser(username=username, email=email, last_name=last_name, first_name=first_name,
                           patronymic=patronymic, birth_day=birth_day, is_publisher=True, foto=foto, password=password)

            if CustomUser.objects.filter(username=username).exists():
                messages.success(request, 'Пользователь с таким логином уже существует')
                return redirect('aluser')
            else:
                a.save()
                messages.success(request, 'Аккаунт успешно создан')
                return redirect('aluser')

        elif userType == "Преподаватель":
            a = CustomUser(username=username, email=email, last_name=last_name, first_name=first_name,
                           patronymic=patronymic, birth_day=birth_day, is_librarian=True, foto=foto, password=password)

            if CustomUser.objects.filter(username=username).exists():
                messages.success(request, 'Пользователь с таким логином уже существует')
                return redirect('aluser')
            else:
                a.save()
                messages.success(request, 'Аккаунт успешно создан')
                return redirect('aluser')

        else:
            messages.error(request, 'Ошибка, попробуйте позже')
            return redirect('userform')
    else:
        return redirect('userform')


class AFeedback(LoginRequiredMixin, ListView):
    model = Feedback
    template_name = 'dashboard/questions.html'
    context_object_name = 'feedbacks'
    paginate_by = 10

    def get_queryset(self):
        return Feedback.objects.order_by('-id')


class ALViewAnswerAdmin(LoginRequiredMixin, DetailView):
    model = Feedback
    template_name = 'dashboard/detailquestion.html'


class AnswerForms(LoginRequiredMixin, UpdateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'dashboard/answerquestion.html'
    success_url = reverse_lazy('afeedback')


@login_required
def send_answer(request):
    if request.method == 'POST':
        fioA = request.POST['fioA']
        emailA = request.POST['emailA']
        temaA = request.POST['temaA']
        answer = request.POST['answer']
        userTypeA = request.POST['userTypeA']

        recepients = [emailA,]

        a = Answer(fioA=fioA, emailA=emailA, temaA=temaA, answer=answer, userTypeA=userTypeA)
        a.save()

        try:
            text = get_template('dashboard/email.html')
            html = get_template('dashboard/email.html')
            context = {'fioA' : fioA, 'answer' : answer}
            text_content = text.render(context)
            html_content = html.render(context)

            msg = EmailMultiAlternatives(temaA, text_content, 'dashenka-ostapenko@mail.ru', recepients)
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
        except BadHeaderError:  # Защита от уязвимости
            return HttpResponse('Произошла ошибка, попробуйте позже')

        messages.success(request, 'Ответ успешно отправлен')

        return redirect('afeedback')

    else:
        messages.error(request, 'Произошла ошибка, попробуйте позже')
        return redirect('answer_form')


class DashNewsListView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'dashboard/allnews.html'
    context_object_name = 'news'
    paginate_by = 10


    def get_queryset(self):
        return News.objects.order_by('-id')


class ADViewNews(LoginRequiredMixin, DetailView):
    model = News
    template_name = 'dashboard/detailnews.html'


class ADeleteNews(SuccessMessageMixin, DeleteView):
    model = News
    template_name = 'dashboard/deletenews.html'
    success_url = reverse_lazy('dash_news')
    success_message = 'Новость успешно удалена'


@login_required
def lanews_form(request):
    return render(request, 'dashboard/addnews.html')


@login_required
def lanews(request):
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        cover = request.FILES['cover']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        a = News(title=title, text=text, cover=cover, uploaded_by=username, user_id=user_id)
        a.save()
        messages.success(request, 'Новость успешно добавлена')
        return redirect('dash_news')
    else:
        messages.error(request, 'Произошла ошибка, попробуйте позже')
        return redirect('lanews_form')


@login_required
def aabout(request):
    return render(request, 'dashboard/about.html')


@login_required
def asearch(request):
    query = request.GET['query']
    print(type(query))

    # data = query.split()
    data = query
    print(len(data))
    if (len(data) == 0):
        return redirect('dashboard')
    else:
        a = data

        # Searching for It
        qs1 = models.Book.objects.filter(title__iexact=a).distinct()
        qs2 = models.Book.objects.filter(title__iexact=a).distinct()
        qs3 = models.Book.objects.all().filter(title__contains=a)
        qs4 = models.Book.objects.select_related().filter(title__contains=a).distinct()
        qs5 = models.Book.objects.filter(title__startswith=a).distinct()
        qs6 = models.Book.objects.filter(title__endswith=a).distinct()
        qs7 = models.Book.objects.filter(title__istartswith=a).distinct()
        qs8 = models.Book.objects.all().filter(title__icontains=a)
        qs9 = models.Book.objects.filter(title__iendswith=a).distinct()

        qs10 = models.Book.objects.filter(author__iexact=a).distinct()
        qs11 = models.Book.objects.filter(author__iexact=a).distinct()
        qs12 = models.Book.objects.all().filter(author__contains=a)
        qs13 = models.Book.objects.select_related().filter(author__contains=a).distinct()
        qs14 = models.Book.objects.filter(author__startswith=a).distinct()
        qs15 = models.Book.objects.filter(author__endswith=a).distinct()
        qs16 = models.Book.objects.filter(author__istartswith=a).distinct()
        qs17 = models.Book.objects.all().filter(author__icontains=a)
        qs18 = models.Book.objects.filter(author__iendswith=a).distinct()

        qs19 = models.Book.objects.filter(year__iexact=a).distinct()
        qs20 = models.Book.objects.filter(year__iexact=a).distinct()
        qs21 = models.Book.objects.all().filter(year__contains=a)
        qs22 = models.Book.objects.select_related().filter(year__contains=a).distinct()
        qs23 = models.Book.objects.filter(year__startswith=a).distinct()
        qs24 = models.Book.objects.filter(year__endswith=a).distinct()
        qs25 = models.Book.objects.filter(year__istartswith=a).distinct()
        qs26 = models.Book.objects.all().filter(year__icontains=a)
        qs27 = models.Book.objects.filter(year__iendswith=a).distinct()

        qs28 = models.Book.objects.filter(publisher__iexact=a).distinct()
        qs29 = models.Book.objects.filter(publisher__iexact=a).distinct()
        qs30 = models.Book.objects.all().filter(publisher__contains=a)
        qs31 = models.Book.objects.select_related().filter(publisher__contains=a).distinct()
        qs32 = models.Book.objects.filter(publisher__startswith=a).distinct()
        qs33 = models.Book.objects.filter(publisher__endswith=a).distinct()
        qs34 = models.Book.objects.filter(publisher__istartswith=a).distinct()
        qs35 = models.Book.objects.all().filter(publisher__icontains=a)
        qs36 = models.Book.objects.filter(publisher__iendswith=a).distinct()

        files = itertools.chain(qs1, qs2, qs3, qs4, qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13, qs14, qs15, qs16,
                                qs17, qs18, qs19, qs20, qs21, qs22, qs23, qs24, qs25, qs26, qs27, qs28, qs29, qs30, qs31,
                                qs32, qs33, qs34, qs35, qs36)

        res = []
        for i in files:
            if i not in res:
                res.append(i)

        print(res)
        files = res

        page = request.GET.get('page', 1)
        paginator = Paginator(files, 12)
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)

        if files:
            return render(request, 'dashboard/searchresult.html', {'files': files})
        return render(request, 'dashboard/searchresult.html', {'files': files})