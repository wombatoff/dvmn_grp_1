from datetime import date

from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from users.models import CustomUser


class Storage(models.Model):
    locality = models.CharField('Населенный пункт', max_length=50)
    address = models.CharField('Адрес', max_length=255)
    short_description = models.CharField('Короткое описание', max_length=50)
    temperature = models.IntegerField('Температура на складе')
    main_image = models.ImageField('Основное изображение')
    small_image = models.ImageField('Маленькое изображение')
    contacts = models.TextField('Контакты', blank=True)
    information = models.TextField('Информация', blank=True)
    directions_to_storage = models.TextField('Как добраться', blank=True)

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f'{self.locality}, {self.address}'

    def total_boxes_count(self):
        return self.boxes.count()

    def available_boxes_count(self):
        return self.boxes.filter(is_available=True).count()

    def max_boxing_height(self):
        return self.boxes.aggregate(models.Max('height'))['height__max']

    def min_boxing_price(self):
        return self.boxes.aggregate(models.Min('price'))['price__min']


class Box(models.Model):
    number = models.CharField('Номер', max_length=50)
    floor = models.PositiveIntegerField('Этаж')
    length = models.PositiveIntegerField('Длина')
    width = models.PositiveIntegerField('Ширина')
    height = models.DecimalField('Высота', max_digits=2, decimal_places=1)
    area = models.DecimalField('Площадь', max_digits=3, decimal_places=1, editable=False)
    price = models.IntegerField('Стоимость')
    is_available = models.BooleanField(default=True)
    storage = models.ForeignKey(
        Storage,
        verbose_name='Склад',
        related_name='boxes',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return self.number

    def update_availability(self):
        today = date.today()
        bookings = Orders.objects.filter(box=self, end_rental_date__gte=today)
        self.is_available = not bookings.exists()
        self.save()


@receiver(pre_save, sender=Box)
def update_area(sender, instance, **kwargs):
    instance.area = instance.length * instance.width


class Orders(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Клиент', on_delete=models.CASCADE)
    box = models.ForeignKey(Box, verbose_name='Бокс', on_delete=models.CASCADE)
    rental_date = models.DateField('Дата аренды')
    rental_period_months = models.PositiveIntegerField('Срок аренды, месяцев')
    end_rental_date = models.DateField('Дата окончания аренды', blank=True, null=True)

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'

    def __str__(self):
        return f'{self.user.email}, бокс {self.box.number}'


@receiver(pre_save, sender=Orders)
def update_end_rental_date(sender, instance, **kwargs):
    instance.end_rental_date = instance.rental_date + relativedelta(months=instance.rental_period_months)
