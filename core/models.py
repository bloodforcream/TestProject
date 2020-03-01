from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    inn = models.CharField(max_length=12, blank=True, null=True, validators=[MinLengthValidator(10)],
                           verbose_name='ИНН')
    account = models.FloatField(verbose_name='Счет в рублях', default=0, blank=True)

    def clean(self):
        if self.inn is not None and not self.inn.isnumeric():
            raise ValidationError('ИНН должен состоять только из цифр')

    def __str__(self):
        return f'{self.user.get_username()}, {self.inn}'
