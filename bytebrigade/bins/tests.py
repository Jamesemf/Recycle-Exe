from django.test import TestCase, Client

# Create your tests here.
class TestPages(TestCase):
    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['newHome'] = 'XFI-LEC'
        session.save()

    def test_get_bin_map_view(self):
        response = self.client.get('/bins/bin/map/')
        self.assertEqual(response.status_code, 200)

    def test_post_bin_map_view(self):
        response = self.client.post('/bins/bin/map/')
        self.assertEqual(response.redirect_chain, [('/scanner/recycle/confirm/', 302), ('/account/login/', 302)])

    def test_get_bin_nav_view(self):
        response = self.client.get('/bins/bin/map/nav')
        self.assertEqual(response.status_code, 200)

    def test_get_bin_nav_arrive(self):
        response = self.client.get('/bins/bin/map/arrive')
        self.assertEqual(response.status_code, 200)
