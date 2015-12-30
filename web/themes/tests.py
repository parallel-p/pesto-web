from django.test import TestCase, Client
from .models import *
from stats.models import *
from .themes_by_user import *

# Create your tests here.
class TestThemesByUser(TestCase):
    def test_common(self):
        u = User(first_name='f', last_name='l')
        u.save()
        s1 = Season(name='s1', year=2001, order=1)
        s1.save()
        s2 = Season(name='s2', year=2002, order=2)
        s2.save()
        p = Parallel(name='p1')
        p.save()
        part1 = Participation(user=u, season=s1, parallel=p)
        part2 = Participation(user=u, season=s2, parallel=p)
        part1.save()
        part2.save()
        t1 = Theme(name='t1')
        t2 = Theme(name='t2')
        t1.save()
        t2.save()
        ur1 = UserResult(participation=part1, theme=t1, solved=1)
        ur2 = UserResult(participation=part1, theme=t2, solved=2)
        ur3 = UserResult(participation=part2, theme=t1, solved=3)
        ur1.save()
        ur2.save()
        ur3.save()
        res = str(themes_by_user(1))
        good = '[PartResult("s1 p1", [[\'t2\', 2], [\'t1\', 1]]), PartResult("s2 p1", [[\'t1\', 3]])]'
        self.assertEqual(res, good)
        
    def test_no_result(self):
        u = User(first_name='f', last_name='l')
        u.save()
        s1 = Season(name='s1', year=2001, order=1)
        s1.save()
        s2 = Season(name='s2', year=2002, order=2)
        s2.save()
        p = Parallel(name='p1')
        p.save()
        part1 = Participation(user=u, season=s1, parallel=p)
        part2 = Participation(user=u, season=s2, parallel=p)
        part1.save()
        part2.save()
        t1 = Theme(name='t1')
        t2 = Theme(name='t2')
        t1.save()
        t2.save()
        ur1 = UserResult(participation=part1, theme=t1, solved=1)
        ur2 = UserResult(participation=part1, theme=t2, solved=2)
        ur1.save()
        ur2.save()
        res = str(themes_by_user(1))
        good = '[PartResult("s1 p1", [[\'t2\', 2], [\'t1\', 1]])]'
        self.assertEqual(res, good)