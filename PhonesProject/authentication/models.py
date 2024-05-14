from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str, is_staff: bool = False):
        """
        Creates a new user with given parameters and returns the created model.
        """
        if email is None:
            raise TypeError('Exception: username is None.')
        elif isinstance(email, str) and not email.strip():
            raise ValueError("Exception: empty email.")

        if password is None:
            raise TypeError('Exception: password is None.')
        elif isinstance(password, str) and not password.strip():
            raise ValueError("Exception: empty password.")

        user = self.model(email=email, is_staff=is_staff)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str):
        """ Creates an admin, is_staff is True """
        user = self.create_user(email, password, True)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, max_length=255, unique=True, verbose_name="Почта", null=False, blank=False)
    password = models.CharField(max_length=255, validators=[MinLengthValidator(8)], verbose_name="Пароль")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'is_staff']

    objects = UserManager()

    def __str__(self):
        s = ""
        if self.is_staff:
            s = " +staff"
        return f"User email:{self.email}" + s

    def get_full_name(self):
        """ Default method that returns only username instead of using name and surname. """
        return self.email

    def get_short_name(self):
        """ Default method that returns only username instead of using name and surname. """
        return self.email[: self.email.index("@")]
