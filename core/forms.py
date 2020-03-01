from django import forms
from django.contrib.auth.models import User

from core.models import Profile


class TransferForm(forms.ModelForm):
    user_from = forms.ChoiceField(choices=[], label='Отправитель')
    amount = forms.FloatField(label='Сумма')
    field_order = ['user_from', 'inn', 'account']

    class Meta:
        model = Profile
        fields = ('inn',)
        labels = {
            'inn': 'ИНН получателей'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_users_choices()

    def set_users_choices(self):
        self.fields['user_from'].choices = [(user, user) for user in User.objects.all()]
