from django.test import TestCase
from .doreshka_by_user import doreshka_by_user_str, doreshka_by_user_seconds, get_rating
from .models import *
from stats.models import User


class TestDoreshkaByUser(TestCase):
    def test_common(self):
        u1 = User(first_name='f', last_name='l')
        u1.save()
        ur1 = UserResult(user=u1, average_time=12345)
        ur1.save()
        self.assertEqual(doreshka_by_user_str(u1.id), '3 часа 25 минут')
        self.assertEqual(doreshka_by_user_seconds(u1.id), 12345)
        u2 = User(first_name='f', last_name='l')
        u2.save()
        ur3 = UserResult(user=u2, average_time=3720)
        ur3.save()
        self.assertEqual(doreshka_by_user_str(u2.id), '1 час 2 минуты')
        self.assertEqual(doreshka_by_user_seconds(u2.id), 3720)
        u3 = User(first_name='f', last_name='l')
        u3.save()
        ur3 = UserResult(user=u3, average_time=18665)
        ur3.save()
        self.assertEqual(doreshka_by_user_str(u3.id), '5 часов 11 минут')
        self.assertEqual(doreshka_by_user_seconds(u3.id), 18665)
        
        self.assertEqual(get_rating(), [
            (1, u3, '5 часов 11 минут'),
            (2, u1, '3 часа 25 минут'),
            (3, u2, '1 час 2 минуты')
        ])
