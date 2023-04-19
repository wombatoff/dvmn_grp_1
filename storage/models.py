from django.db import models


class Storage(models.Model):
    address = models.CharField('Адрес', max_length=255, db_index=True)
    description = models.CharField('Описание', max_length=255)
    direction = models.CharField('Как проехать', max_length=255)
    temperature = models.IntegerField('Температура на складе')
    ceiling_height = models.DecimalField('Высота потолка', max_digits=3, decimal_places=2)
    min_price = models.IntegerField('Минимальная стоимость')
    image = models.ImageField('Изображение')

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.address


class Box(models.Model):
    number = models.CharField('Номер', max_length=50, db_index=True)
    floor = models.IntegerField('Этаж')
    length = models.IntegerField('Длина')
    width = models.IntegerField('Ширина')
    height = models.IntegerField('Высота')
    price = models.IntegerField('Стоимость')
    is_available = models.BooleanField('Доступен')
    storage = models.ForeignKey(
        Storage,
        verbose_name='Склад',
        related_name='boxes',
        db_index=True
    )

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return self.number

    def square(self):
        return self.length * self.width


class Contact(models.Model):
    name = models.CharField('Имя', max_length=50)
    phonenumber = PhoneNumberField(verbose_name='Номер телефона', db_index=True)
    location = models.ForeignKey(
        Location,
        verbose_name='Локация',
        related_name='contacts',
        db_index=True
    )

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.name