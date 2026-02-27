from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from assets.models import * 

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ("role", "department"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            "fields": ("role", "department"),
        }),
    )
admin.site.register(User, CustomUserAdmin)
admin.site.register(Asset)
admin.site.register(MaintenanceLog)





