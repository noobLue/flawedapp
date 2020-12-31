from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='pages/login.html')),
	path('logout/', LogoutView.as_view(next_page='/')),

    path('init', views.init_user_data, name='init'),
    path('send',views.send_message),
    path('view', views.view_messages),

    path('sql', views.sql_injection, name='sql'),
    path('email', views.change_email, name = 'email'),
]