from django.contrib import admin
from .models import CreatedGroup, FutureModerator
# Register your models here.


class CreatedGroupAdmin(admin.ModelAdmin):
    model = CreatedGroup


class FutureModeratorAdmin(admin.ModelAdmin):
    model = FutureModerator


admin.site.register(CreatedGroup, CreatedGroupAdmin)
admin.site.register(FutureModerator, FutureModeratorAdmin)
