from django.test import TestCase
from django.urls import reverse

from .models import Cup, Don, User


class CupTests(TestCase):
    def setUp(self):
        a, b, c = (User.objects.create_user(guy, email='%s@example.org' % guy, password=guy) for guy in 'abc')
        x = Cup(name='X', mini=1000)
        x.save()
        y = Cup(name='Y', mini=1200)
        y.save()
        Don(cup=x, user=a, maxi=100).save()
        Don(cup=x, user=b, maxi=50, mini=10).save()
        Don(cup=y, user=a, maxi=800).save()
        Don(cup=y, user=b, maxi=600, mini=200).save()
        Don(cup=y, user=c, maxi=400).save()

    # MODELS

    def test_str(self):
        self.assertEqual(str(Cup.objects.first()), 'Cup pour X')
        self.assertEqual(str(Don.objects.first()), 'Don de a pour X')

    def test_get_absolute_url(self):
        self.assertEqual(Don.objects.first().get_absolute_url(), '/cup/x')

    def test_funded(self):
        x, y = Cup.objects.all()
        self.assertFalse(x.funded())
        self.assertTrue(y.funded())

    def test_missing(self):
        self.assertEqual(Cup.objects.first().missing(), 850)

    def test_effort(self):
        self.assertEqual(Cup.objects.get(name='Y').effort(), 0.625)

    def test_pays(self):
        a, b, c = User.objects.all()
        cup = Cup.objects.get(name='Y')
        self.assertEqual(a.don_set.get(cup=cup).pays(), 500)
        self.assertEqual(b.don_set.get(cup=cup).pays(), 450)
        self.assertEqual(c.don_set.get(cup=cup).pays(), 250)

    # VIEWS

    def test_list_cup(self):
        self.assertEqual(self.client.get(reverse('cup:home')).status_code, 200)

    def test_create_cup(self):
        self.client.login(username='a', password='a')
        self.assertEqual(self.client.post(reverse('cup:add'), {'name': 'Z', 'mini': 42}).status_code, 302)
        self.assertEqual(Cup.objects.get(name='Z').mini, 42)

    def test_dispatch_update_don(self):
        self.assertEqual(Don.objects.first().maxi, 100)
        self.client.login(username='a', password='a')
        r = self.client.get(reverse('cup:don', kwargs={'slug': 'x'}))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('cup:update_don', kwargs={'slug': 'x', 'pk': 1}))
        self.assertEqual(self.client.post(r.url, {'maxi': 200, 'mini': 50}).status_code, 302)
        self.assertEqual(Don.objects.first().maxi, 200)

    def test_dispatch_create_don(self):
        self.client.login(username='c', password='c')
        r = self.client.get(reverse('cup:don', kwargs={'slug': 'x'}))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('cup:add_don', kwargs={'slug': 'x'}))
        self.assertEqual(self.client.post(r.url, {'maxi': 500}).status_code, 200)
        # self.assertEqual(Don.objects.last().maxi, 500)
