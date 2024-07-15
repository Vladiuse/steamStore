from django.contrib import admin
from .models import SteamPayReplenishment, SteamPayReplenishmentCode, SteamAccount


class SteamPayReplenishmentCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'type', 'available']

class SteamAccountAdmin(admin.ModelAdmin):
    list_display = ['key', 'price', 'description',]


admin.site.register(SteamPayReplenishment)
admin.site.register(SteamPayReplenishmentCode, SteamPayReplenishmentCodeAdmin)
admin.site.register(SteamAccount, SteamAccountAdmin)


