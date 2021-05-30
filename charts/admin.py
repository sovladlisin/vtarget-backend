from django.contrib import admin

from .models import Cabinet, Chart, Medal, Table
# Register your models here.


class CabinetAdmin(admin.ModelAdmin):
    model = Cabinet


class ChartAdmin(admin.ModelAdmin):
    model = Chart


class MedalAdmin(admin.ModelAdmin):
    model = Medal


class TableAdmin(admin.ModelAdmin):
    model = Table


admin.site.register(Cabinet, CabinetAdmin)
admin.site.register(Chart, ChartAdmin)
admin.site.register(Medal, MedalAdmin)
admin.site.register(Table, TableAdmin)
