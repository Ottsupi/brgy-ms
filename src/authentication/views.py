from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .forms import UserLoginForm, UserRegistrationForm
from .models import UserManager


def registration_view(request: HttpRequest):
    form = UserRegistrationForm(request.POST or None)
    context = {
        "form": form,
    }

    if form.is_valid():
        phone_number = form.cleaned_data.get("phone_number")
        password = form.cleaned_data.get("password")
        first_name = form.cleaned_data.get("first_name")
        middle_name = form.cleaned_data.get("middle_name")
        last_name = form.cleaned_data.get("last_name")

        user_manager: UserManager = get_user_model().objects
        user_manager.create_user(
            phone_number=phone_number,
            password=password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
        )

    return render(request, "authentication/register.html", context)


def login_view(request: HttpRequest):
    form = UserLoginForm(request.POST or None)
    context = {
        "form": form,
    }

    if form.is_valid():
        credentials: dict[str, str] = {
            "username": form.cleaned_data.get("phone_number"),
            "password": form.cleaned_data.get("password"),
        }

        user = authenticate(request, **credentials)
        if user is not None:
            login(request, user)
            return redirect("/")

        error_message = "No account found with the given phone number and password"
        error = forms.ValidationError(error_message, code="invalid")
        form.add_error(None, error)

    return render(request, "authentication/login.html", context)


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("/")
