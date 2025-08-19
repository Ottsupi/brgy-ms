from django import forms

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
        model = User
        fields = (
            "phone_number",
            "email",
            "first_name",
            "middle_name",
            "last_name",
        )
