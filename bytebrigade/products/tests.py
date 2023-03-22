import validators

from django.contrib.auth.models import User
from django.test import TestCase, Client

from account.models import Statistic
from products.models import Product
from bins.models import BinData
from home.models import Transaction

from products.views import product_image


# Create your tests here.

class TestNotLoggedIn(TestCase):
    def setUp(self):
        self.client = Client()

    def test_product_create(self):
        response = self.client.get('/product/create/', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

    def test_product(self):
        response = self.client.get('/product/', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

    def test_product_dex(self):
        response = self.client.get('/product/dex', follow=True)
        self.assertEqual(response.redirect_chain, [('/product/dex/', 301), ('/account/login/', 302)])


class TestLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testUser', password='PassTest')
        self.stat = Statistic.objects.create(user=self.user)
        self.prod = Product.objects.create(barcode='1', name='testName', weight='0.3', material='Paper', recycle='True')
        self.bin = BinData.objects.create(binId='1', binName='testBin', binLat='50.7358441920794000000000',
                               binLong='-3.5297260384419000000000', bin_paper='True')
        self.transaction = Transaction.objects.create(user=self.user, product=self.prod, bin=self.bin)
        self.client.login(username='testUser', password='PassTest')

    def tearDown(self):
        self.client.logout()

    def test_product_create_logged(self):
        session = self.client.session
        session['barcode'] = 1
        session['pokedex_barcode'] = -1
        session.save()
        response = self.client.post('/product/create/', {'barcode': '4060900109798', 'name': '7up Free',
                                                          'weight': '500', 'material': 'Plastic', 'recycle': 'True'},
                                    follow=True)
        self.assertEquals(self.stat.lastRecycle, self.prod)
        self.assertEqual(response.redirect_chain, [('/product/', 302)])

    def test_get_product_create_logged(self):
        session = self.client.session
        session['barcode'] = 1
        session.save()
        response = self.client.get('/product/create/', follow=True)
        self.assertEquals(response.redirect_chain, [('/', 302)])

    def test_product_logged(self):
        session = self.client.session
        session['barcode'] = 1
        session.save()
        response = self.client.post('/product/', {'location_lat': '50.7358441920794000000000',
                                                   'location_long': '-3.5297260384419000000000'}, follow=True)
        self.assertEqual(response.redirect_chain, [('/bin/map/', 302)])

    def test_get_product_logged(self):
        session = self.client.session
        session['barcode'] = 1
        session['pokedex_barcode'] = -1
        session.save()
        response = self.client.get('/product/')
        self.assertEqual(response.context['present_button'], 1)
        self.assertEqual(response.status_code, 200)

    def test_get_product_logged_pokedex_barcode_valid(self):
        session = self.client.session
        session['barcode'] = 1
        session['pokedex_barcode'] = 1
        session.save()
        response = self.client.get('/product/')
        self.assertEqual(response.context['present_button'], 0)
        self.assertEqual(response.status_code, 200)


    def test_product_dex_logged(self):
        session = self.client.session
        session['barcode'] = -1
        session.save()
        response = self.client.post('/product/dex/', {'barcode': '1'}, follow=True)
        self.assertEqual(response.redirect_chain, [('/product/', 302)])

    def test_get_product_dex_logged(self):
        response = self.client.get('/product/dex/')
        self.assertEqual(response.context['product'], {self.prod: 1})

    def test_product_image(self):
        image = product_image("test")
        self.assertEqual(validators.url(image), True)
