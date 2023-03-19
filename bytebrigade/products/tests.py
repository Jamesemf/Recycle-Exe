from django.contrib.auth.models import User
from django.test import TestCase, Client

from account.models import Statistic
from products.models import Product
from bins.models import BinData


# Create your tests here.

class TestNotLoggedIn(TestCase):
    def setUp(self):
        self.client = Client()

    def test_products_create(self):
        response = self.client.get('/products/create/', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

    def test_products(self):
        response = self.client.get('/products/', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])


class TestLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testUser', password='PassTest')
        self.stat = Statistic.objects.create(user=self.user)
        self.prod = Product.objects.create(barcode='1', name='testName', weight='0.3', material='Paper', recycle='True')
        self.bin = BinData.objects.create(binId='1', binName='testBin', binLat='50.7358441920794000000000',
                               binLong='-3.5297260384419000000000', bin_paper='True')
        self.client.login(username='testUser', password='PassTest')

    def tearDown(self):
        self.client.logout()

    def test_products_create(self):
        session = self.client.session
        session['barcode'] = 1
        session.save()
        response = self.client.post('/products/create/', {'barcode': '4060900109798', 'name': '7up Free',
                                                          'weight': '500', 'material': 'Plastic', 'recycle': 'True'},
                                    follow=True)
        self.assertEqual(response.redirect_chain, [('/products/', 302)])

    def test_get_products_create(self):
        session = self.client.session
        session['barcode'] = 1
        session.save()
        response = self.client.get('/products/create/', follow=True)
        self.assertEquals(response.redirect_chain, [('/', 302)])

    def test_products(self):
        session = self.client.session
        session['barcode'] = 1
        session.save()
        response = self.client.post('/products/', {'location_lat': '50.7358441920794000000000',
                                                   'location_long': '-3.5297260384419000000000'}, follow=True)
        self.assertEqual(response.redirect_chain, [('/bins/bin/map/', 302)])

    def test_get_products(self):
        session = self.client.session
        session['barcode'] = 1
        session.save()
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

