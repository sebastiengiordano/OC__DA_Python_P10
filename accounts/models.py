from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class CustomUserManager(BaseUserManager):
    '''This class aims to managed our CustomUser.'''

    def create_user(self, first_name, last_name, email, password=None):
        """
        Creates and saves a User with the given email , first_name,
        last_name and password.
        """
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)  # change password to hash
        user.admin = False
        user.staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        """
        Creates and saves a superuser with the given email , first_name,
        last_name and password.
        """
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)  # change password to hash
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    '''This class aims to defined our own customized user.'''

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True)
    first_name = models.CharField(
        verbose_name='first name',
        max_length=255)
    last_name = models.CharField(
        verbose_name='last name',
        max_length=255)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    # Since Email & Password are required by default,
    # there's no need to add in REQUIRED_FIELDS.
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        unique_together = ('first_name', 'last_name')

    def __str__(self):
        return f"{self.email}"

    @staticmethod
    def has_perm(perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @staticmethod
    def has_module_perms(app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff
