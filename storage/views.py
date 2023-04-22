from datetime import date, timedelta

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from storage.models import Box, Storage, Rental
from django.db.models import Prefetch, Count, Sum
from .forms import RentalForm


def index(request):
    return render(request, 'storage/index.html')


@login_required
def my_rent(request):
    user = request.user
    rentals = Rental.objects.filter(user=user)
    context = {'rentals': rentals}
    return render(request, 'storage/my-rent.html', context)


def boxes(request):
    return render(request, 'storage/boxes.html')


def faq(request):
    return render(request, 'storage/faq.html')


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


@login_required
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


@login_required
def boxes(request, storage_id):
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


def rent_box(request, box_id):
    if request.method == 'GET':
        return render(request, 'storage/create-order.html', {'form': RentalForm()})
    else:
        selected_box = get_object_or_404(Box, id=box_id)
        if not selected_box.is_available:
            return HttpResponse('Коробка уже занята')
        form = RentalForm(request.POST)
        if form.is_valid():
            form = RentalForm(request.POST)
            newrental = form.save(commit=False)
            newrental.user = request.user
            newrental.box = selected_box
            newrental.save()
            selected_box.is_available = False
            selected_box.save()
            return redirect('storage:my_rent')
        else:
            error = f"Ошибка. Убедидесь что дата начала аренды не раньше {date.today()}," \
                    f"а дата окончания не раньше {date.today() + timedelta(days=30)}"
            return render(request, 'storage/create-order.html', {'form': form, 'error': error})
