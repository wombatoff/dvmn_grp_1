from django.shortcuts import render, redirect
from storage.models import Box, Storage
from django.db.models import Prefetch, Count, Sum


def get_boxes_context(storage):
    storage_boxes = storage.boxes.all()

    boxes_to_3 = []
    boxes_to_10 = []
    boxes_from_10 = []

    for box in storage_boxes:
        if box.square() < 3:
            box.sq = box.square()
            boxes_to_3.append(box)
        elif box.square() < 10:
            box.sq = box.square()
            boxes_to_10.append(box)
        else:
            box.sq = box.square()
            boxes_from_10.append(box)

    all_boxes = boxes_to_3 + boxes_to_10 + boxes_from_10

    context = {
        'boxes_to_3': boxes_to_3,
        'boxes_to_10': boxes_to_10,
        'boxes_from_10': boxes_from_10,
        'all_boxes': all_boxes,
    }
    return context


def storages(request):
    storages = Storage.objects.prefetch_related(
        Prefetch('boxes', queryset=Box.objects.filter(is_available=True))
    ).annotate(
        total_boxes=Count('boxes'),
        available_boxes=Sum('boxes__is_available')
    )
    storage = storages[0]

    context = {'storages': storages, 'storage': storage}
    boxes_context = get_boxes_context(storage)
    context.update(boxes_context)
    return render(request, 'storage/boxes.html', context)


def boxes(request, storage_id=1):
    try:
        selected_storage = Storage.objects.prefetch_related(
            Prefetch('boxes', queryset=Box.objects.filter(is_available=True))
        ).annotate(total_boxes=Count('boxes'), available_boxes=Sum('boxes__is_available')).get(id=storage_id)

    except Storage.DoesNotExist:
        return redirect('storages')

    storages = Storage.objects.prefetch_related(
        Prefetch('boxes', queryset=Box.objects.filter(is_available=True))
    ).annotate(
        total_boxes=Count('boxes'),
        available_boxes=Sum('boxes__is_available')
    )

    context = {'selected_storage': selected_storage, 'storages': storages}
    boxes_context = get_boxes_context(selected_storage)
    context.update(boxes_context)

    return render(request, 'storage/boxes.html', context=context)