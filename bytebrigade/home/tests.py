from django.contrib.auth.models import User
from django.test import TestCase, Client


# Create your tests here.
class TestNotLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get('', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

    def test_instruction(self):
        response = self.client.get('/instruction/')
        self.assertEqual(response.status_code, 200)

    def test_leaderboard(self):
        response = self.client.get('/leaderboard/', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])


# Test pages when user is logged in
class TestLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testUser', password='PassTest')
        self.client.login(username='testUser', password='PassTest')

    def test_home_logged(self):
        response = self.client.get('', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_instruction_logged(self):
        response = self.client.get('/instruction/')
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_logged(self):
        response = self.client.get('/leaderboard/', follow=True)
        self.assertEqual(response.status_code, 200)
