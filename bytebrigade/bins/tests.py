from django.contrib.auth.models import User
from django.test import TestCase, Client

from bins.models import BinData


# Create your tests here.
class TestPages(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_bin_map_view(self):
        response = self.client.get('/bin/map/', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])

    def test_get_bin_nav_view(self):
        response = self.client.get('/bin/nav/', follow=True)
        self.assertEqual(response.redirect_chain, [('/account/login/', 302)])


class TestLoggedIn(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testUser', password='PassTest')
        self.bin = BinData.objects.create(binId='XFI-LEC', binName='XFI Building Lecture',
                                          binLat='50.7358441920794000000000', binLong='-3.5297260384419000000000',
                                          bin_general='True', bin_cans='True', bin_plastic='True')
        session = self.client.session
        session['newHome'] = 'XFI-LEC'
        session['shownMap'] = 1
        session.save()
        self.client.login(username='testUser', password='PassTest')

    def test_get_bin_map_view_logged(self):
        response = self.client.get('/bin/map/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['bin'], self.bin)
        self.assertEqual(response.context['presentButton'], 1)

    def test_post_bin_map_view_logged(self):
        response = self.client.post('/bin/map/', follow=True)
        self.assertEqual(response.redirect_chain[0], ('/bin/nav/', 302))

    def test_get_bin_nav_view_logged(self):
        response = self.client.get('/bin/nav/')
        self.assertEqual(response.status_code, 200)

    def test_post_bin_nav_view_logged(self):
        response = self.client.post('/bin/nav/', follow=True)
        self.assertEqual(response.redirect_chain[0], ('/scanner/recycle/confirm/', 302))


class TestNewHomeNotSet(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testUser', password='PassTest')
        self.bin = BinData.objects.create(binId='XFI-LEC', binName='XFI Building Lecture',
                                          binLat='50.7358441920794000000000', binLong='-3.5297260384419000000000',
                                          bin_general='True', bin_cans='True', bin_plastic='True')
        session = self.client.session
        session['newHome'] = -1
        session['shownMap'] = -1
        session.save()
        self.client.login(username='testUser', password='PassTest')

    def test_get_bin_map_view_no_new_home(self):
        response = self.client.get('/bin/map/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['Bins'][0], self.bin)
        self.assertEqual(response.context['presentButton'], 0)

    def test_get_bin_nav_view_no_new_home(self):
        response = self.client.get('/bin/nav/', follow=True)
        self.assertEqual(response.redirect_chain, [('/bin/map/', 302)])

