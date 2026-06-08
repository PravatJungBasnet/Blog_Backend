import re
import time

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("password_set", True)
        return self.create_user(email, password, **extra_fields)


class NonDeletedManager(models.Manager):
    def get_queryset(self):
        """Return objects that are not soft-deleted by default"""
        return super().get_queryset().filter(deleted_at__isnull=True)


class NonDeletedUserManager(NonDeletedManager, CustomUserManager):
    pass


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=100, blank=True)
    detail = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_picture/", null=True, blank=True
    )
    ip_address = models.CharField(max_length=100, blank=True)

    password_set = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_active = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = NonDeletedUserManager()
    all_objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.is_active = False
        timestamp = int(time.time())
        self.email = self.email = f"{timestamp}_deleted_{self.email}"

        self.save(using=using)

    def restore(self, using=None, keep_parents=False):
        self.deleted_at = None
        self.is_active = True
        self.email = re.sub(r"\d+_deleted_", "", self.email)
        self.save(using=using)

    def __str__(
        self,
    ):
        if self.deleted_at is not None:
            return "Deleted User"
        else:
            return f"{self.first_name} {self.last_name}"


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_followed = models.BooleanField(default=True)
