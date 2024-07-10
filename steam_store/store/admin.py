from django.contrib import admin
from .models import SteamPayReplenishment, SteamPayReplenishmentCode


class SteamPayReplenishmentCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'type', 'available']


admin.site.register(SteamPayReplenishment)
admin.site.register(SteamPayReplenishmentCode, SteamPayReplenishmentCodeAdmin)
