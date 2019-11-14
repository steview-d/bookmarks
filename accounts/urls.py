from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.urls import path
from accounts.views import register, premium, profile, support, about
from accounts import urls_pw_reset

urlpatterns = [
    # user auth functionality
    path('login/', auth_views.LoginView.as_view(
        template_name="accounts/login.html",
        redirect_authenticated_user=True), name="login"),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='about_page'), name="logout"),
    path('register/', register, name="register"),
    # password reset urls
    path('', include(urls_pw_reset)),
    # user account info
    path('premium/', premium, name='premium'),
    path('profile/', profile, name='profile'),
    path('support/', support, name='support'),
    path('about/', about, name='about'),
]
