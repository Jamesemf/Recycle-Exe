from django.contrib.auth.models import User
from django.test import TestCase, Client

from home.models import Transaction, TransactionLike
from bins.models import BinData
from products.models import Product


# Create your tests here.
class TestNotLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get('', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

    def test_instruction(self):
        response = self.client.get('/abouts/')
        self.assertEqual(response.status_code, 200)

    def test_leaderboard(self):
        response = self.client.get('/leaderboard/', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])


# Test pages when user is logged in
class TestLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testUser', password='PassTest')
        self.user2 = User.objects.create_user(username='testUser2', password='PassTest2')
        self.bin = BinData.objects.create(binId='XFI-LEC', binName='XFI Building Lecture',
                                          binLat='50.7358441920794000000000', binLong='-3.5297260384419000000000',
                                          bin_general='True', bin_cans='True', bin_plastic='True')
        self.prod = Product.objects.create(barcode='1', name='testName', weight='0.3', material='Paper', recycle='True')
        self.transaction = Transaction.objects.create(bin=self.bin, user=self.user, product=self.prod)
        self.transactionLike = TransactionLike.objects.create(user=self.user, transaction=self.transaction)
        self.client.login(username='testUser', password='PassTest')

    def test_home_logged(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['Transaction'][0], self.transaction)
        self.assertEqual(response.context['likedList'][0], 1)

    def test_post_home(self):
        self.client.logout()
        self.client.login(username='testUser2', password='PassTest2')
        response = self.client.post('', {'trans_id': '1'})
        self.assertEqual(TransactionLike.objects.filter(transaction_id=self.transaction.transaction_id)[1].user,
                         self.user2)

    def test_instruction_logged(self):
        response = self.client.get('/abouts/')
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_logged(self):
        response = self.client.get('/leaderboard/', follow=True)
        self.assertEqual(response.status_code, 200)
