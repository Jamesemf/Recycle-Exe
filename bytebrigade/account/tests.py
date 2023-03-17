from django.contrib.auth.models import User
from django.test import TestCase, Client

from account.models import Goal
from account.models import Statistic
from products.models import Product


# Create your tests here.

class TestNotLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()

    def test_account(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)

    def test_account_login(self):
        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 200)

    def test_account_logout(self):
        response = self.client.get('/account/logout/')
        self.assertEqual(response.status_code, 200)

    def test_account_registration(self):
        response = self.client.get('/account/registration/')
        self.assertEqual(response.status_code, 200)

    def test_account_password(self):
        response = self.client.get('/account/password/')
        self.assertEqual(response.status_code, 200)

    def test_account_password_reset(self):
        response = self.client.get('/account/password/reset')
        self.assertEqual(response.status_code, 200)

    def test_account_password_change(self):
        response = self.client.get('/account/password/change')
        self.assertEqual(response.status_code, 302)

    def test_account_password_change_done(self):
        response = self.client.get('/account/password/change/done', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/password/change/done/', 301),
                                                   ('/account/login/?next=/account/password/change/done/', 302)])


# Test account page grants access if user is logged in

class TestLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testUser', password='PassTest')
        self.goal = Goal.objects.create(goalID='1', name='testGoal', description='A test goal', target='100')
        self.stat = Statistic.objects.create(user=self.user)
        self.prod = Product.objects.create(barcode='1', name='testName', weight='0.3', material='Paper', recycle='True')
        self.client.login(username='testUser', password='PassTest')

    def test_account_logged(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)

    def test_account_password_reset_logged(self):
        response = self.client.get('/account/password/reset')
        self.assertEqual(response.status_code, 200)

    def test_account_password_change_logged(self):
        response = self.client.get('/account/password/change')
        self.assertEqual(response.status_code, 200)

    def test_post_account_registration(self):
        response = self.client.post('/account/registration/', {'name': 'testName', 'email': 'testEmail@email.com',
                                                               'password': 'testPass', 'password_confirm': 'testPass'},
                                    follow=True)
        self.assertEqual(response.redirect_chain, [('/', 302)])

    def test_post_account_addUserGoal(self):
        response = self.client.post('/account/addUserGoal/',
                                    {'goalNum': '1', 'goal-options': '1', 'goal-type': 'Recycle'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/account/', 302)])
