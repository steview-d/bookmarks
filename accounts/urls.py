from django.contrib.auth import views as auth_views
from django.urls import path
from accounts.views import logout, register

urlpatterns = [
    path('login', auth_views.LoginView.as_view(
        template_name="accounts/login.html",
        redirect_authenticated_user=True), name="login"),
    path('logout', logout, name="logout"),
    path('register', register, name="register"),
]
