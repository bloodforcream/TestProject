from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    inn = models.IntegerField(verbose_name='ИНН', default=0, blank=True, null=True)
    account = models.FloatField(verbose_name='Счет в рублях', default=0, blank=True, null=True)

    def __str__(self):
        return f'{self.user.get_username()}, {self.inn}'
