from django.urls import path
from .views import (
    RegisterView, UserInfoChangeView,
    logout, SignInView,
    UserPasswordChangeView
    )
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView
)


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', SignInView.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('user/setttings/<str:pk>', UserInfoChangeView.as_view(), name='user-settings'),
    path('user/password/', UserPasswordChangeView.as_view(), name='user-password'),
    path('password/reset', 
        PasswordResetView.as_view(template_name='users/password_reset.html'),
        name='password_reset'),
    path('password/reset/done',
        PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    path('password/reset/confirm',
        PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password/reset/complete', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),
]

