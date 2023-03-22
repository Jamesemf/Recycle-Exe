from django.contrib.auth.models import User
from django.test import TestCase, Client

from products.models import Product
from home.models import Transaction
from bins.models import BinData
from account.models import Statistic

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
        self.bin = BinData.objects.create(binId='XFI-LEC', binName='XFI Building Lecture',
                                          binLat='50.7358441920794000000000', binLong='-3.5297260384419000000000',
                                          bin_general='True', bin_cans='True', bin_plastic='True')
        self.prod = Product.objects.create(barcode='1', name='testName', weight='0.3', material='Paper', recycle='True')
        self.transaction = Transaction.objects.create(bin=self.bin, user=self.user, product=self.prod)
        self.stat = Statistic.objects.create(user=self.user)
        self.client.login(username='testUser', password='PassTest')

    def test_scanner_logged_in(self):
        response = self.client.get('/scanner/')
        self.assertEqual(response.status_code, 200)

    def test_scanner_post_product_exists(self):
        session = self.client.session
        session['barcode'] = 1
        session['pokedex_barcode'] = -1
        session.save()
        response = self.client.post('/scanner/', {'barcode': '1'}, follow=True)
        self.assertEqual(response.redirect_chain, [('/', 302)])

    def test_scanner_post_product_does_not_exist(self):
        self.stat.delete()
        self.prod.delete()
        response = self.client.post('/scanner/', {'barcode': '1'}, follow=True)
        self.assertEqual(response.redirect_chain, [('/product/create/', 302)])

    def test_recycle_confirm_logged_in(self):
        session = self.client.session
        session['valid'] = -1
        session.save()
        response = self.client.get('/scanner/recycle/confirm', follow=True)
        self.assertEqual(response.redirect_chain, [('/scanner/recycle/confirm/', 301), ('/', 302)])

    def test_recycle_confirm_valid_session(self):
        session = self.client.session
        session['valid'] = 1
        session['barcode'] = 1
        session['newHome'] = 'XFI-LEC'
        session['success_recycle'] = 1
        session.save()
        response = self.client.get('/scanner/recycle/confirm', follow=True)
        self.assertEqual(response.redirect_chain[0], ('/scanner/recycle/confirm/', 301))
        self.assertEqual(Transaction.objects.filter(product=self.prod)[1].user, self.user)
        self.assertEqual(Transaction.objects.filter(product=self.prod)[1].bin, self.bin)
        self.assertEqual(response.context['Transaction'][0].transaction_id, 2)
        # Test addstats function in account views
        self.assertEquals(self.stat.lastRecycle, self.prod)
