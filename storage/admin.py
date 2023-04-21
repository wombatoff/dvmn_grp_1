from django.contrib import admin
from .models import Storage, Box, Rental


class BoxInline(admin.TabularInline):
    model = Box


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    inlines = [
        BoxInline
    ]


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    pass


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    pass
