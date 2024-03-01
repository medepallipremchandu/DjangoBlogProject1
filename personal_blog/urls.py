# personal_blog/urls.py

from django.contrib import admin
from django.urls import path, include
from blog.views import ResetPasswordView
from blog import views as user_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path('login/', user_view.Login, name ='login'),
    path('logout/', user_view.logout_view, name='logout'),
    path('register/', user_view.register, name ='register'),
    path('password-reset/', ResetPasswordView.as_view(template_name='blog/password_reset.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'),
         name='password_reset_complete'),
]