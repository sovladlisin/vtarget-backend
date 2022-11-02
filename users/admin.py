from django.contrib import admin
from .models import VkUser, ServiceRequest, ServiceInfo
# Register your models here.


class VkUserAdmin(admin.ModelAdmin):
    model = VkUser

class ServiceRequestAdmin(admin.ModelAdmin):
    model = ServiceRequest

class ServiceInfoAdmin(admin.ModelAdmin):
    model = ServiceInfo

admin.site.register(VkUser, VkUserAdmin)
admin.site.register(ServiceRequest, ServiceRequestAdmin)
admin.site.register(ServiceInfo, ServiceInfoAdmin)
