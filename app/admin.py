from django.contrib import admin
from .models import Services, SSOToken


class ServicesModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'secret_key']
    list_display_links = ['id', 'name']


class SSOTokenModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'token', 'deleted_at']
    list_display_links = ['id', 'token']


admin.site.register(Services, ServicesModelAdmin)
admin.site.register(SSOToken, SSOTokenModelAdmin)
