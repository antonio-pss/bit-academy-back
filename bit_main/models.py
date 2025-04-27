import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


class ModelBase(models.Model):
    id = models.AutoField(
        db_column='id_model',
        primary_key=True,
        blank=False,
        null=False,
    )
    created = models.DateTimeField(
        db_column='created_at',
        auto_now_add=True,
        blank=False,
        null=False,
    )
    modified = models.DateTimeField(
        db_column='modified_at',
        auto_now=True,
        blank=False,
        null=False,
    )
    active = models.BooleanField(
        db_column='active',
        default=True,
        blank=False,
        null=False,
    )

    class Meta:
        abstract = True


class User(ModelBase, AbstractUser):
    username = models.CharField(
        MinLengthValidator(6),
        max_length=12,
        unique=True,
        blank=False,
        null=False,
    )
    name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    password = models.TextField(
        MinLengthValidator(8),
        blank=False,
        null=False,
    )
    xp = models.IntegerField(
        blank=False,
        null=False,
        default=0,
    )
    streak = models.IntegerField(
        blank=False,
        null=False,
        default=0,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
