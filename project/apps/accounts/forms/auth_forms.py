from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class UserLoginForm(AuthenticationForm):
    """
    UserLoginForm Customizing the Django Authentication Form
    """

    username = UsernameField(
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "class": "form-control",
                "placeholder": "name@example.com",
                "id": "floatingInput",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "floatingPassword",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username").lower()
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
