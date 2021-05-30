from django.contrib import admin
from .models import PlannedPost
# Register your models here.


class PlannedPostAdmin(admin.ModelAdmin):
    model = PlannedPost


admin.site.register(PlannedPost, PlannedPostAdmin)
