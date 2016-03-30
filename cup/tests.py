from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Cup, Don, User


class CupTests(TestCase):
    def setUp(self):
        a, b, c = (User.objects.create_user(guy, email='%s@example.org' % guy, password=guy) for guy in 'abc')
        x = Cup(name='X', mini=1000)
        x.save()
        y = Cup(name='Y', mini=1000, maxi=1200)
        y.save()
        Don(cup=x, user=a, maxi=100).save()
        Don(cup=x, user=b, maxi=50, mini=10).save()
        Don(cup=y, user=a, maxi=700).save()
        Don(cup=y, user=b, maxi=500, mini=100).save()
        Don(cup=y, user=c, maxi=600).save()

    # MODELS

    def test_str(self):
        self.assertEqual(str(Cup.objects.first()), 'Cup pour X')
        self.assertEqual(str(Don.objects.first()), 'Don de a pour X')

    def test_funded(self):
        x, y = Cup.objects.all()
        self.assertFalse(x.funded())
        self.assertTrue(y.funded())

    def test_missing(self):
        self.assertEqual(Cup.objects.first().missing(), 850)

    # VIEWS

    def test_cup_list(self):
        self.assertEqual(self.client.get(reverse('cup:home')).status_code, 200)

    # def test_
