from django.test import TestCase
from .doreshka_by_user import doreshka_by_user
from .models import *
from stats.models import User


class TestDoreshkaByUser(TestCase):
    def test_common(self):
        u1 = User(first_name='f', last_name='l')
        u1.save()
        ur1 = UserResult(user=u1, average_time=12345)
        ur1.save()
        self.assertEqual(doreshka_by_user(u1.id), '3 часа 25 минут')
        u2 = User(first_name='f', last_name='l')
        u2.save()
        ur3 = UserResult(user=u2, average_time=3720)
        ur3.save()
        self.assertEqual(doreshka_by_user(u2.id), '1 час 2 минуты')
        u3 = User(first_name='f', last_name='l')
        u3.save()
        ur3 = UserResult(user=u3, average_time=18665)
        ur3.save()
        self.assertEqual(doreshka_by_user(u3.id), '5 часов 11 минут')