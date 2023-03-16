import unittest
from django.test import TestCase, Client


# Create your tests here.

class TestNotLoggedIn(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_products_create(self):
        response = self.client.get('/products/create/')
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

    def test_products(self):
        response = self.client.get('/products/')
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])


class TestLoggedIn(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username='cameron', password='PopTest')

    def test_products_create(self):
        session = self.client.session
        session['barcode'] = 8930472417339
        session.save()
        response = self.client.post('/products/create/', {'barcode': '4060900109798', 'name': '7up Free',
                                                          'weight': '500', 'material': 'Plastic', 'recycle': 'True'},
                                    follow=True)
        self.assertEqual(response.redirect_chain, [('/products/', 302)])

    def test_get_products_create(self):
        response = self.client.get('/products/create/')
        self.assertEquals(response.redirect_chain, [('/', 302)])

    def test_products(self):
        session = self.client.session
        session['barcode'] = 8930472417339
        session.save()
        response = self.client.post('/products/', {'location_lat': '50.7358441920794000000000',
                                                   'location_long': '-3.5297260384419000000000'}, follow=True)
        self.assertEqual(response.redirect_chain, ['/bins/bin/map/', 302])

    def test_get_products(self):
        session = self.client.session
        session['barcode'] = 8930472417339
        session.save()
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
