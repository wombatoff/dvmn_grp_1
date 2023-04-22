from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from users.models import CustomUser


class Storage(models.Model):
    locality = models.CharField('Населенный пункт', max_length=50, db_index=True)
    address = models.CharField('Адрес', max_length=255, db_index=True)
    short_description = models.CharField('Короткое описание', max_length=50)
    temperature = models.IntegerField('Температура на складе')
    ceiling_height = models.DecimalField('Высота потолка', max_digits=3, decimal_places=2)
    min_price = models.IntegerField('Минимальная стоимость')
    first_image = models.ImageField('Основное изображение')
    second_image = models.ImageField('Второе изображение')

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f'{self.locality} {self.address}'


class Box(models.Model):
    number = models.CharField('Номер', max_length=50, db_index=True)
    floor = models.IntegerField('Этаж')
    length = models.IntegerField('Длина')
    width = models.IntegerField('Ширина')
    height = models.DecimalField('Высота', max_digits=2, decimal_places=1)
    price = models.IntegerField('Стоимость')
    is_available = models.BooleanField('Доступен', default=True)
    storage = models.ForeignKey(
        Storage,
        verbose_name='Склад',
        related_name='boxes',
        db_index=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return self.number

    def square(self):
        return self.length * self.width


class Rental(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Клиент', on_delete=models.CASCADE, related_name='user')
    box = models.ForeignKey(Box, verbose_name='Бокс', on_delete=models.CASCADE, related_name='rentals')
    start_date = models.DateField('Дата начала аренды')
    end_date = models.DateField('Дата окончания аренды')


    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'

    def __str__(self):
        return self.box.number
