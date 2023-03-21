from django.contrib.auth.models import User
from django.test import TestCase, Client

from shop.models import ShopItems
from account.models import Statistic
from products.models import Product

# Create your tests here.

class TestNotLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()

    def test_shop(self):
        response = self.client.get('/shop/', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

class TestLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testUser', password='PassTest')
        self.shopItems = ShopItems.objects.create(name='testShopItems', cost='1', description='A test shop item')
        self.prod = Product.objects.create(barcode='1', name='testName', weight='0.3', material='Paper', recycle='True')
        self.client.login(username='testUser', password='PassTest')

    def test_get_shop(self):
        response = self.client.get('/shop/')
        self.assertEqual(response.status_code, 200)

    def test_post_shop_cant_afford(self):
        self.stat = Statistic.objects.create(user=self.user)
        response = self.client.post('/shop/', {'shop_item': '1'})
        self.assertEqual(response.status_code, 200)

    def test_post_shop_can_afford(self):
        self.stat = Statistic.objects.create(user=self.user, points='2')
        response = self.client.post('/shop/', {'shop_item': '1'})
        self.assertEqual(response.status_code, 200)
