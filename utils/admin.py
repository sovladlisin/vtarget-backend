from django.contrib import admin
from .models import CollectTagsJob
# Register your models here.


class CollectTagsJobAdmin(admin.ModelAdmin):
    model = CollectTagsJob


admin.site.register(CollectTagsJob, CollectTagsJobAdmin)
