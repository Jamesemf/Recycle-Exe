from django.contrib.auth.models import User
from django.test import TestCase, Client

from products.models import Product


# Create your tests here.

class TestNotLoggedIn(TestCase):
    # Test pages when user is not logged in
    def setUp(self):
        self.client = Client()

    def test_scanner(self):
        response = self.client.get('/scanner/', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

    def test_recycle_confirm(self):
        response = self.client.get('/scanner/recycle/confirm', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/scanner/recycle/confirm/', 301), ('/account/login/', 302)])


class TestLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testUser', password='PassTest')
        self.client.login(username='testUser', password='PassTest')

    def test_scanner_logged_in(self):
        response = self.client.get('/scanner/')
        self.assertEqual(response.status_code, 200)

    def test_scanner_post_product_exists(self):
        self.prod = Product.objects.create(barcode='1', name='testName', weight='0.3', material='Paper', recycle='True')
        response = self.client.post('/scanner/', {'barcode': '1'}, follow=True)
        self.assertEqual(response.redirect_chain, [('/products/', 302)])

    def test_scanner_post_product_does_not_exist(self):
        response = self.client.post('/scanner/', {'barcode': '1'}, follow=True)
        self.assertEqual(response.redirect_chain, [('/products/create/', 302)])

    def test_recycle_confirm_logged_in(self):
        session = self.client.session
        session['valid'] = -1
        session.save()
        response = self.client.get('/scanner/recycle/confirm', follow=True)
        self.assertEqual(response.redirect_chain, [('/scanner/recycle/confirm/', 301), ('/', 302)])

    def test_recycle_confirm_valid_session(self):
        session = self.client.session
        session['valid'] = 1
        session['barcode'] = 500128584364
        session['newHome'] = 'XFI-LEC'
        session.save()
        response = self.client.get('/scanner/recycle/confirm', follow=True)
        self.assertEqual(response.redirect_chain, [('/scanner/recycle/confirm/', 301), ('/', 302)])
