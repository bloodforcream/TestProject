from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from unittest.mock import patch

from core.tools import transfer_to_inn


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.user = User.objects.create(username='TestUser')

    def test_home_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_home_POST(self):
        with patch('core.views.transfer_to_inn') as mocked_transfer:
            mocked_transfer.return_value = 'Успешный перевод'
            response = self.client.post(self.home_url, data={
                'user_from': self.user,
                'inn_to': '12',
                'amount': '12',
            })

            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'core/home.html')
            self.assertEquals(response.context['response'], 'Успешный перевод')


class TransferTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='TestUser')
        self.target_user = User.objects.create(username='TestUserTarget')

    def test_transfer_to_inn_one_inn(self):
        self.set_up_users()
        data = {
            'user_from': self.user,
            'inn_to': 567,
            'amount': 10
        }
        self.assertEquals(transfer_to_inn(data), '10 рублей переведенно одному пользователю')

    def test_transfer_to_inn_multiple_inn(self):
        self.target_user2 = User.objects.create(username='TestUserTarget2')
        self.target_user2.profile.inn = '567'
        self.target_user2.profile.save()
        self.set_up_users()
        data = {
            'user_from': self.user,
            'inn_to': 567,
            'amount': 10
        }
        self.assertEquals(transfer_to_inn(data), '2 пользователям переведенно по 5.0 рублей')

    def test_transfer_to_inn_negative_amount(self):
        self.set_up_users()
        data = {
            'user_from': self.user,
            'inn_to': 567,
            'amount': -3
        }
        self.assertEquals(transfer_to_inn(data), 'Введите положительную сумму')

    def test_transfer_to_inn_invalid_inn(self):
        self.set_up_users()
        data = {
            'user_from': self.user,
            'inn_to': 333,
            'amount': 10
        }
        self.assertEquals(transfer_to_inn(data), 'Нет пользователей с таким ИНН')

    def test_transfer_to_inn_not_enough_money(self):
        self.set_up_users()
        data = {
            'user_from': self.user,
            'inn_to': 333,
            'amount': 5555
        }
        self.assertEquals(transfer_to_inn(data), 'У пользователя недостаточно средств')

    def set_up_users(self):
        self.user.profile.account = 999
        self.user.profile.save()
        self.target_user.profile.inn = '567'
        self.target_user.profile.save()
