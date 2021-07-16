from django.contrib import admin
from .models import AccountDuplicateJob
# Register your models here.


class AccountDuplicateJobAdmin(admin.ModelAdmin):
    model = AccountDuplicateJob


admin.site.register(AccountDuplicateJob, AccountDuplicateJobAdmin)
