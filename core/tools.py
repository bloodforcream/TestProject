from core.models import Profile
from django.contrib.auth.models import User


def transfer_to_inn(data):
    user_from = User.objects.get(username=data.get('user_from'))
    inn_to = data.get('inn_to')
    amount = data.get('amount')
    all_profiles = Profile.objects.all()

    if user_from.profile.account >= amount:
        transfer_to = all_profiles.filter(inn=inn_to)
        if transfer_to.first():
            if amount >= 0:
                user_from.profile.account -= amount
                user_from.save()
                for profile in transfer_to:
                    profile.account += amount / transfer_to.count()
                    profile.save()
                if transfer_to.count() > 1:
                    return f'{transfer_to.count()} пользователям переведенно по {amount / transfer_to.count()} рублей'
                else:
                    return f'{amount} рублей переведенно одному пользователю'
            else:
                return 'Введите положительную сумму'
        else:
            return 'Нет пользователей с таким ИНН'
    else:
        return 'У пользователя недостаточно средств'
