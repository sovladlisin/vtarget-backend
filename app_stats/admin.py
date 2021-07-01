from django.contrib import admin
from .models import AppsIds
# Register your models here.


class AppsIdsAdmin(admin.ModelAdmin):
    model = AppsIds


admin.site.register(AppsIds, AppsIdsAdmin)
