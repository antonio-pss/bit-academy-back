from django.contrib import admin

from core import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    exclude = ()
