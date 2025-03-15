import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


class TenantManager(BaseUserManager):
    def create_user(self, name, password=None, **extra_fields):
        if not name:
            raise ValueError("The name field must be set")
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(name, password, **extra_fields)


class Tenant(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)

    objects = TenantManager()

    USERNAME_FIELD = "name"

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
