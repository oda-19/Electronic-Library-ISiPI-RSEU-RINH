from django.urls import path
from . import views




urlpatterns = [

# Общие
 path('', views.main, name='home'),
 path('login_form/', views.login_form, name='login_form'),
 path('login/', views.loginView, name='login'),
 path('logout/', views.logoutView, name='logout'),
 path('regform/', views.register_form, name='regform'),
 path('register/', views.registerView, name='register'),
 path('publisher/', views.UBookListView.as_view(), name='publisher'),
 path('uvbook/<int:pk>', views.UViewBook.as_view(), name='uvbook'),
 path('feedback_form/', views.feedback_form, name='feedback_form'),
 path('send_feedback/', views.send_feedback, name='send_feedback'),
 path('news/', views.NewsListView.as_view(), name='news'),
 path('avnews/<int:pk>', views.AViewNews.as_view(), name='avnews'),
 path('about/', views.about, name='about'),
 path('usearch/', views.usearch, name='usearch'),


 # Преподаватель
 path('librarian/', views.LBookListView.as_view(), name='librarian'),
 path('labook_form/', views.labook_form, name='labook_form'),
 path('labook/', views.labook, name='labook'),
 path('lsearch/', views.lsearch, name='lsearch'),


 # Студент
 path('alvuser/<int:pk>', views.ALViewUser.as_view(), name='alvuser'),


 # Администратор
 path('ahome/', views.amain, name='ahome'),
 path('alvusera/<int:pk>', views.ALViewUserAdmin.as_view(), name='alvusera'),
 path('dashboard/', views.ABookListView.as_view(), name='dashboard'),
 path('avbook/<int:pk>', views.AViewBook.as_view(), name='avbook'),
 path('aebook/<int:pk>', views.AEditView.as_view(), name='aebook'),
 path('adbook/<int:pk>', views.ADeleteBook.as_view(), name='adbook'),
 path('aabook_form/', views.aabook_form, name='aabook_form'),
 path('aabook/', views.aabook, name='aabook'),
 path('aluser/', views.ListUserView.as_view(), name='aluser'),
 path('userform/', views.user_form, name='userform'),
 path('userreg/', views.userView, name='userreg'),
 path('aduser/<int:pk>', views.ADeleteUser.as_view(), name='aduser'),
 path('afeedback/', views.AFeedback.as_view(), name='afeedback'),
 path('avanswer/<int:pk>', views.ALViewAnswerAdmin.as_view(), name='avanswer'),
 path('answer_form/<int:pk>', views.AnswerForms.as_view(), name='answer_form'),
 path('send_answer/', views.send_answer, name='send_answer'),
 path('dash_news/', views.DashNewsListView.as_view(), name='dash_news'),
 path('avdnews/<int:pk>', views.ADViewNews.as_view(), name='avdnews'),
 path('adelnews/<int:pk>', views.ADeleteNews.as_view(), name='adelnews'),
 path('lanews_form/', views.lanews_form, name='lanews_form'),
 path('lanews/', views.lanews, name='lanews'),
 path('aabout/', views.aabout, name='aabout'),
 path('asearch/', views.asearch, name='asearch'),

]