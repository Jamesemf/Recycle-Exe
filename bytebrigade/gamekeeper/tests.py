from django.contrib.auth.models import User
from django.test import TestCase, Client

from bins.models import BinData
from account.models import Goal, Statistic
from shop.models import ShopItems
from products.models import Product


# Create your tests here.

class TestNotLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()

    def test_gamekeeper(self):
        response = self.client.get('/gamekeeper/', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

    def test_gamekeeper_addBin(self):
        response = self.client.get('/gamekeeper/addBin', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

    def test_gamekeeper_addGoal(self):
        response = self.client.get('/gamekeeper/addGoal', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

    def test_gamekeeper_addShopItem(self):
        response = self.client.get('/gamekeeper/addShopItem', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

    def test_gamekeeper_deleteBin(self):
        response = self.client.get('/gamekeeper/deleteBin', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

    def test_gamekeeper_deleteGoal(self):
        response = self.client.get('/gamekeeper/deleteGoal', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

    def test_gamekeeper_deleteShopItem(self):
        response = self.client.get('/gamekeeper/deleteShopItem', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])


class TestLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testUser', password='PassTest')
        self.client.login(username='testUser', password='PassTest')

    def test_gamekeeper_logged(self):
        response = self.client.get('/gamekeeper/', follow=True)
        self.assertEqual(response.redirect_chain, ([('/', 302)]))

    def test_gamekeeper_addBin_logged(self):
        response = self.client.get('/gamekeeper/addBin', follow=True)
        self.assertEqual(response.redirect_chain, [('/', 302)])

    def test_gamekeeper_addGoal_logged(self):
        response = self.client.get('/gamekeeper/addGoal', follow=True)
        self.assertEqual(response.redirect_chain, [('/', 302)])

    def test_gamekeeper_addShopItem_logged(self):
        response = self.client.get('/gamekeeper/addShopItem', follow=True)
        self.assertEqual(response.redirect_chain, [('/', 302)])

    def test_gamekeeper_deleteBin_logged(self):
        response = self.client.get('/gamekeeper/deleteBin', follow=True)
        self.assertEqual(response.redirect_chain, [('/', 302)])

    def test_gamekeeper_deleteGoal_logged(self):
        response = self.client.get('/gamekeeper/deleteGoal', follow=True)
        self.assertEqual(response.redirect_chain, [('/', 302)])

    def test_gamekeeper_deleteShopItem_logged(self):
        response = self.client.get('/gamekeeper/deleteShopItem', follow=True)
        self.assertEqual(response.redirect_chain, [('/', 302)])


class TestAdmin(TestCase):

    def setUp(self):
        self.client = Client()
        self.adminuser = User.objects.create_user(username='testAdminUser', password='PassAdminTest')
        self.user = User.objects.create_user(username='testUser', password='PassTest')
        self.adminuser.is_superuser = True
        self.adminuser.save()
        self.client.login(username='testAdminUser', password='PassAdminTest')
        self.goal = Goal.objects.create(goalID='1', name='testGoal', description='A test goal', target='100')
        self.shopItems = ShopItems.objects.create(name='testShopItems', cost='1', description='A test shop item',
                                                  stock='1')
        self.bin = BinData.objects.create(binId='XFI-LEC', binName='XFI Building Lecture',
                                          binLat='50.7358441920794000000000', binLong='-3.5297260384419000000000',
                                          bin_general='True', bin_cans='True', bin_plastic='True')
        self.prod = Product.objects.create(barcode='1', name='testName', weight='0.3', material='Paper', recycle='True')
        self.stat = Statistic.objects.create(user=self.user, carbon='10')

    def test_gamekeeper_admin(self):
        response = self.client.get('/gamekeeper/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['Goals'][0].goalID, 1)
        self.assertEqual(response.context['ShopItems'][0].item_id, 1)
        self.assertEqual(response.context['Bins'][0].binId, 'XFI-LEC')

    def test_gamekeeper_addBin_admin(self):
        response = self.client.post('/gamekeeper/addBin', {'binId': 'ROWE', 'binName': 'Rowe House Bin shed',
                                                           'binLat': '50.7342910385844000000000',
                                                           'binLong': '3.5285127459301700000000',
                                                           'bin_general': 'True', 'bin_recycle': 'True',
                                                           'bin_paper': 'True', 'bin_cans': 'True',
                                                           'bin_glass': 'True', 'bin_plastic': 'True'}, follow=True)
        self.assertEqual(BinData.objects.get(binId='ROWE').binName, 'Rowe House Bin shed')
        self.assertEqual(response.redirect_chain, [('/gamekeeper/', 302)])

    def test_gamekeeper_addGoal_admin(self):
        response = self.client.post('/gamekeeper/addGoal',
                                    {'name': 'testGoal2', 'description': 'A second test goal', 'target': '200'},
                                    follow=True)
        self.assertEqual(Goal.objects.get(goalID=2).description, 'A second test goal')
        self.assertEqual(response.redirect_chain, [('/gamekeeper/', 302)])

    def test_gamekeeper_addShopItem_admin(self):
        response = self.client.post('/gamekeeper/addShopItem',
                                    {'name': 'testShopItems2', 'description': 'A second test shop item', 'cost': '2',
                                     'stock': '1'},
                                    follow=True)
        self.assertEqual(ShopItems.objects.get(item_id=2).description, 'A second test shop item')
        self.assertEqual(response.redirect_chain, [('/gamekeeper/', 302)])

    def test_gamekeeper_deleteBin_admin(self):
        response = self.client.post('/gamekeeper/deleteBin', {'bin': 'XFI-LEC'}, follow=True)
        self.assertEqual(BinData.objects.all().count(), 0)
        self.assertEqual(response.redirect_chain, [('/gamekeeper/', 302)])

    def test_gamekeeper_deleteGoal_admin(self):
        response = self.client.post('/gamekeeper/deleteGoal', {'goal': '1'}, follow=True)
        self.assertEqual(Goal.objects.all().count(), 0)
        self.assertEqual(response.redirect_chain, [('/gamekeeper/', 302)])

    def test_gamekeeper_deleteShopItem_admin(self):
        response = self.client.post('/gamekeeper/deleteShopItem', {'shopItem': '1'}, follow=True)
        self.assertEqual(ShopItems.objects.all().count(), 0)
        self.assertEqual(response.redirect_chain, [('/gamekeeper/', 302)])
