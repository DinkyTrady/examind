from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, username, password):
        if not username:
            raise ValueError("The Email field must be set")

        user = self.model(
            email=self.normalize_email(email), full_name=full_name, username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, username, password, role="admin"):
        user = self.create_user(
            email=email,
            full_name=full_name,
            username=username,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# Create your models here.
class User(AbstractBaseUser):
    ROLE_CHOICES = {("siswa", "Siswa"), ("guru", "Guru"), ("admin", "Admin")}

    full_name = models.CharField(max_length=250, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=120)
    email = models.EmailField(max_length=150, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="admin")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "full_name",
        "email",
    ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    def get_short_name(self):
        return self.email.split("@")[0]


class Siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kelas = models.CharField(max_length=10)
    nis = models.CharField(max_length=25)

    def username(self):
        return self.user.username

    def full_name(self):
        return self.user.full_name

    def email(self):
        return self.user.email

    def save(self, *args, **kwargs):
        self.user.role = "siswa"
        return super().save(*args, **kwargs)


class Guru(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nip = models.CharField(max_length=25)

    def save(self, *args, **kwargs):
        self.user.role = "guru"
        return super().save(*args, **kwargs)
