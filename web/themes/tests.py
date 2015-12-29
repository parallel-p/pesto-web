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
        res = themes_by_user(None, 1)
        good = '''<style>
.stats td{vertical-align:top}
.themes td{border:1px solid gray;padding:2px;}
.themes{border-collapse:collapse}
</style>
<table class="stats"><tr>

    <td><b>s1 p1:</b> <table class="themes">
    
        <tr><td>t2</td><td>2</td></tr>
    
        <tr><td>t1</td><td>1</td></tr>
    
    </table></td>

    <td><b>s2 p1:</b> <table class="themes">
    
        <tr><td>t1</td><td>3</td></tr>
    
    </table></td>

</tr></table>
'''
        self.assertEqual(res.strip(), good.strip())
        
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
        res = themes_by_user(None, 1)
        good = '''<style>
.stats td{vertical-align:top}
.themes td{border:1px solid gray;padding:2px;}
.themes{border-collapse:collapse}
</style>
<table class="stats"><tr>

    <td><b>s1 p1:</b> <table class="themes">
    
        <tr><td>t2</td><td>2</td></tr>
    
        <tr><td>t1</td><td>1</td></tr>
    
    </table></td>

</tr></table>
'''
        self.assertEqual(res.strip(), good.strip())