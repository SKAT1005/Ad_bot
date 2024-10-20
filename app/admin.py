from django.contrib import admin

from .models import User, Ad


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    pass
