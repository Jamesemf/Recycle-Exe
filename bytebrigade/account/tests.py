from django.contrib.auth.models import User
from django.test import TestCase, Client

from account.models import Goal, Statistic, UserGoal
from products.models import Product

from account.views import reset_week, reset_month, reset_year

from freezegun import freeze_time


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

    def test_account_password_reset_email_sent(self):
        response = self.client.get('/account/password/reset/emailsent')
        self.assertEqual(response.status_code, 200)

    def test_account_password_reset_complete(self):
        response = self.client.get('/account/password/reset/complete/')
        self.assertEqual(response.status_code, 200)

    def test_account_password_change(self):
        response = self.client.get('/account/password/change')
        self.assertEqual(response.status_code, 302)

    def test_account_password_change_done(self):
        response = self.client.get('/account/password/change/done', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/password/change/done/', 301),
                                                   ('/account/login/?next=/account/password/change/done/', 302)])

    def test_registration_post_match(self):
        # Test that registration page returns 200 if passwords match
        response = self.client.post('/account/registration/', {'name': 'testName', 'email': 'testEmail@email.com',
                                                               'password': 'testPass', 'password_confirm': 'testPass'},
                                    )
        self.assertEqual(response.status_code, 200)

    def test_registration_post_not_match(self):
        # Test that registration page returns 200 if passwords do not match
        response = self.client.post('/account/registration/', {'name': 'testName', 'email': 'testEmail@email.com',
                                                               'password': 'testPass',
                                                               'password_confirm': 'testPassNotMatch'},
                                    )
        self.assertEqual(response.status_code, 200)


class TestLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testUser', password='PassTest')
        self.goal = Goal.objects.create(goalID='1', name='testGoal', description='A test goal', target='100')
        self.stat = Statistic.objects.create(user=self.user, curweek='10', curmonth='10', curyear='10')
        self.prod = Product.objects.create(barcode='1', name='testName', weight='0.3', material='Paper', recycle='True')
        self.client.login(username='testUser', password='PassTest')

    def test_account_logged(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['Profile'], Statistic.objects.get(user=self.user))

    def test_account_password_reset_logged(self):
        response = self.client.get('/account/password/reset')
        self.assertEqual(response.status_code, 200)

    def test_account_password_change_logged(self):
        response = self.client.get('/account/password/change')
        self.assertEqual(response.status_code, 200)

    def test_account_registration_logged(self):
        response = self.client.get('/account/registration/', follow=True)
        self.assertEqual(response.redirect_chain, [('/', 302)])


    def test_post_account_addUserGoal(self):
        response = self.client.post('/account/addUserGoal/',
                                    {'goalNum': '1', 'goal-options': '1', 'goal-type': 'Recycle'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/account/', 302)])
        self.assertEqual(UserGoal.objects.get(user=self.user).goal.goalID, 1)
        # Test if user goal updates

    def test_reset_week(self):
        reset_week()
        response = self.client.get('/account/')
        self.assertEqual(response.context['Profile'].curweek, 0)

    @freeze_time("2023-01-01")
    def test_reset_month(self):
        reset_month()
        response = self.client.get('/account/')
        self.assertEqual(response.context['Profile'].curmonth, 0)

    @freeze_time("2023-01-01")
    def test_reset_month(self):
        reset_year()
        response = self.client.get('/account/')
        self.assertEqual(response.context['Profile'].curyear, 0)



