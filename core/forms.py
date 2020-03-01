from django import forms
from django.contrib.auth.models import User


class TransferForm(forms.Form):
    user_from = forms.ChoiceField(choices=[])
    inn_to = forms.IntegerField()
    amount = forms.FloatField()

    def set_users_choices(self):
        self.fields['user_from'].choices = [(user, user) for user in User.objects.all()]
