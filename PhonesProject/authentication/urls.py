from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, re_path, reverse_lazy
from .views import SignInView, SignUpView, logout_view, profile_view, email_reset_view

app_name = 'authentication'

urlpatterns = [
    path('email-reset', email_reset_view, name='email_reset'),
    path('profile', profile_view, name='profile'),
    re_path(r'^sign-in', SignInView.as_view(), name="sign_in"),
    re_path(r'^sign-up', SignUpView.as_view(), name="sign_up"),
    re_path(r'logout', logout_view, name="sign_out"),
    path('password-reset',
         PasswordResetView.as_view(
          template_name="authentication/password_reset.html",
          email_template_name="authentication/password_reset_email.html",
          success_url=reverse_lazy("authentication:password_reset_done")
         ),
         name="password_reset"),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="authentication/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="authentication/password_reset_confirm.html",
             success_url=reverse_lazy("authentication:password_reset_complete")
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="authentication/password_reset_complete.html"),
         name='password_reset_complete'),
]
