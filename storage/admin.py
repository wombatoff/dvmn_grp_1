from django.contrib import admin

from .models import Storage, Box, Orders


class BoxInline(admin.TabularInline):
    model = Box


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = (
        'locality',
        'address',
        'total_boxes',
        'available_boxes',
        'max_boxing_height',
        'min_boxing_price'
    )

    def total_boxes(self, obj):
        return obj.total_boxes_count()

    total_boxes.short_description = 'Всего боксов'

    def available_boxes(self, obj):
        return obj.available_boxes_count()

    available_boxes.short_description = 'Свободных боксов'


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'floor',
        'length',
        'width',
        'height',
        'area',
        'price',
        'is_available',
        'storage'
    )


@admin.register(Orders)
class RentalAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'box',
        'rental_date',
        'rental_period_months',
        'end_rental_date',
    )
