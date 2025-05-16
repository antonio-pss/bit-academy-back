from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from core.managers import UserManager


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
    password = models.CharField(
        MinLengthValidator(8),
        blank=False,
        null=False,
    )
    xp = models.IntegerField(
        validators=[MinValueValidator(0)],
        blank=False,
        null=False,
        default=0,
    )
    streak = models.IntegerField(
        validators=[MinValueValidator(0)],
        blank=False,
        null=False,
        default=0,
    )
    bio = models.TextField(
        db_column="tx_bio",
        blank=True,
        null=True,
    )
    avatar = models.URLField(
        db_column="url_avatar",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        managed = True
        db_table = 'user'


class Image(ModelBase):
    image_url = models.URLField(
        db_column='image',
        null=True,
        blank=True
    )

    class Meta:
        managed = True
        db_table = 'image'
