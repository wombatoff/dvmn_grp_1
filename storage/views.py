from django.shortcuts import render
from django.shortcuts import render
from storage.models import Box, Storage
from django.db.models import Prefetch, Count, Sum


def view_storages(request):
    storages = Storage.objects.prefetch_related(
        Prefetch('boxes', queryset=Box.objects.filter(is_available=True))
    ).annotate(
        total_boxes=Count('boxes'),
        available_boxes=Sum('boxes__is_available')
    )

    context = {'storages': storages}
    return render(request, 'storage/boxes.html', context)
