from django.contrib.auth.views import LoginView, LogoutView
from ..forms import UserLoginForm

from django.conf import settings
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)


class CustomLoginView(LoginView):
    """
    Display the custom login form and handle the login action.
    """

    form_class = UserLoginForm
    authentication_form = UserLoginForm
    template_name = "login.html"
    redirect_authenticated_user = False
    extra_context = None


class CustomLogoutView(LogoutView):
    """
    Log out the user and display the login page
    """

    template_name = "login.html"
