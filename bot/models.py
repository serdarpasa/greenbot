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


class Autoline(models.Model):
    pass


class Europochta(models.Model):
    pass


class PersonalOrder(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    order_type = models.CharField(max_length=256, null=True)


class GroupOrder(models.Model):
    pass
