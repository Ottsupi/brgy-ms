from django import forms
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField

from .models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
    )

    class Meta:
        model: User = get_user_model()
        fields = (
            "phone_number",
            "email",
            "first_name",
            "middle_name",
            "last_name",
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            error_message = "Passwords does not match"
            error = forms.ValidationError(error_message, code="invalid")
            self.add_error("password", error)
            self.add_error("confirm_password", error)

        return cleaned_data


class UserLoginForm(forms.Form):
    phone_number = PhoneNumberField(
        label="Phone Number",
        widget=forms.TextInput(
            attrs={
                "placeholder": "+63 9XX XXX XXXX",
            },
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "*********",
            },
        ),
    )
