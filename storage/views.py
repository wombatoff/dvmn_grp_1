import base64
from datetime import date

import qrcode
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from storage.models import Storage, Orders, Box
from .forms import RentBoxForm


def index(request):
    return render(request, 'storage/index.html')


@login_required
def my_orders(request):
    user = request.user
    orders = Orders.objects.filter(user=user)
    context = {'orders': orders}
    return render(request, 'storage/my-rent.html', context)


def boxes(request):
    return render(request, 'storage/boxes.html')


def faq(request):
    return render(request, 'storage/faq.html')


@login_required
def storage(request, storage_id=None):
    if storage_id is None:
        current_storage = Storage.objects.first()
    else:
        current_storage = get_object_or_404(Storage, id=storage_id)
    storages = Storage.objects.all()
    current_boxes = current_storage.boxes.filter(is_available=True)

    context = {
        'current_storage': current_storage,
        'storages': storages,
        'all_boxes': current_boxes,
        'to_3_boxes': current_boxes.filter(area__lte=3),
        'to_10_boxes': current_boxes.filter(area__lte=10),
        'up_10_boxes': current_boxes.filter(area__gt=10),
    }
    return render(request, 'storage/boxes.html', context)


@login_required
def rent_box(request, box_id):
    box = get_object_or_404(Box, id=box_id)
    user = request.user

    if request.method == 'POST':
        form = RentBoxForm(request.POST)

        if form.is_valid():
            rental_period_months = form.cleaned_data['rental_period_months']
            phone = form.cleaned_data['phone']

            if phone:
                user.phone = phone
                user.save()

            order = Orders(
                user=user,
                box=box,
                rental_date=date.today(),
                rental_period_months=rental_period_months)
            order.save()
            box.update_availability()
            return redirect('storage:order_success')

    else:
        form = RentBoxForm(initial={'phone': user.phone})

    return render(request, 'storage/rent_box.html', {'form': form, 'box': box})


def order_success(request):
    return render(request, 'storage/order_success.html')

@login_required
def qr_code(request, box_id):
    box = get_object_or_404(Box, id=box_id)
    qr_code_data = box.number
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_code_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    img_io = BytesIO()
    qr_img.save(img_io, format='PNG')
    img_io.seek(0)
    qr_bytes = img_io.read()
    qr_base64 = base64.b64encode(qr_bytes).decode('utf-8')

    return render(request, 'storage/qr-qode.html', context={'qr_code': qr_base64})
