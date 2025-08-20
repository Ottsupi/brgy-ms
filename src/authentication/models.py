# ruff: noqa: EM101, TRY003

from __future__ import annotations

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(
        self,
        *args,
        phone_number: str,
        password: str,
        email: str | None = None,
        first_name: str,
        middle_name: str,
        last_name: str,
        is_active: bool = True,
        is_staff: bool = False,
        is_superuser: bool = False,
    ) -> User:
        if not phone_number:
            raise ValueError("Users must have a phone number")
        if not password:
            raise ValueError("Users must have a password")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not middle_name:
            raise ValueError("Users must have a middle name")
        if not last_name:
            raise ValueError("Users must have a last name")

        # Make sure email is None if not provided
        email = None if email is None or "" else self.normalize_email(email)

        user: User = self.model(
            phone_number=phone_number,
            email=email,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        *args,
        phone_number: str,
        password: str,
        email: str | None = None,
        first_name: str,
        middle_name: str,
        last_name: str,
    ) -> User:
        return self.create_user(
            phone_number=phone_number,
            password=password,
            email=email,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(_("phone number"), unique=True)
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True, default=None)

    first_name = models.CharField(_("first name"), max_length=50)
    middle_name = models.CharField(_("middle name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff"), default=False)
    is_superuser = models.BooleanField(_("superuser"), default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ("first_name", "middle_name", "last_name")

    objects = UserManager()

    def get_full_name(self):
        return f"{self.last_name}, {self.first_name} {self.middle_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return f"{self.phone_number} - {self.last_name}"
