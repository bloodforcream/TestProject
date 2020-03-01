from django.db import transaction

from core.models import Profile
from django.contrib.auth.models import User


def transfer_to_inn(data):
    user_from = User.objects.get(username=data.get('user_from'))
    inn_to = data.get('inn')
    amount = data.get('amount')
    all_profiles = Profile.objects.all()
    if amount <= 0:
        return 'Введите положительную сумму'

    if user_from.profile.account <= amount:
        return 'У пользователя недостаточно средств'

    transfer_to = all_profiles.filter(inn=inn_to)
    if transfer_to.exists() is False:
        return 'Нет пользователей с таким ИНН'

    with transaction.atomic():
        user_from.profile.account -= amount
        user_from.save()
        num_of_target_users = transfer_to.count()
        for profile in transfer_to:
            profile.account += amount / num_of_target_users
            profile.save()
        if num_of_target_users > 1:
            return f'{num_of_target_users} пользователям переведенно по {amount / num_of_target_users} рублей'
        return f'{amount} рублей переведенно одному пользователю'
