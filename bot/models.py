from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    adress = models.TextField(null=True,
                              blank=True,
                              verbose_name='Физический адресс клиента')
    phone = models.CharField(max_length=18,
                             verbose_name='Номер телефона',
                             help_text='Телефон в формате +375291234567')
    email = models.EmailField(verbose_name='Почта/email',
                              unique=True,
                              blank=False)
    first_name = models.CharField(verbose_name='Имя',
                                  max_length=30,
                                  blank=False)
    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=30,
                                 blank=False)
    patronymic = models.CharField(verbose_name='Отчество',
                                  max_length=30,
                                  blank=True,
                                  help_text='Пустое поле если отчества нет')
    telegram_id = models.IntegerField(null=True)
    chat_id = models.IntegerField(null=True)


class TelegramUser(models.Model):
    user_code = models.IntegerField()
    chat_code = models.IntegerField()
    username = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    patronymic = models.CharField(max_length=128)
    address = models.TextField()
    tel = models.CharField(max_length=32)
    data = models.TextField()


class Autoline(models.Model):
    pass


class Europochta(models.Model):
    pass


class PersonalOrder(models.Model):
    code = models.CharField(max_length=256, verbose_name='Код индивидуального заказа')
    number = models.CharField(max_length=256, verbose_name='Номер индивидуального заказа')
    creator = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    surname = models.CharField(max_length=256, verbose_name='Фамилия заказчика')
    tel_number = models.CharField(max_length=32, verbose_name='Номер телефона')
    delivery_type = models.CharField(max_length=32)
    delivery_address = models.CharField(max_length=222, null=True)  # placeholder
    comment = models.CharField(max_length=255,
                               null=True,
                               verbose_name='Комментарий')


class GroupOrder(models.Model):
    pass
