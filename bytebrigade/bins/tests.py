from django.test import TestCase, Client

from bins.models import BinData


# Create your tests here.
class TestPages(TestCase):
    def setUp(self):
        self.client = Client()
        self.bin = BinData.objects.create(binId='XFI-LEC', binName='XFI Building Lecture',
                                          binLat='50.7358441920794000000000', binLong='-3.5297260384419000000000',
                                          bin_general='True', bin_cans='True', bin_plastic='True')
        session = self.client.session
        session['newHome'] = 'XFI-LEC'
        session.save()

    def test_get_bin_map_view(self):
        response = self.client.get('/bins/bin/map/')
        self.assertEqual(response.status_code, 200)

    def test_post_bin_map_view(self):
        response = self.client.post('/bins/bin/map/', follow=True)
        self.assertEqual(response.redirect_chain[0], ('/scanner/recycle/confirm/', 302))

    def test_get_bin_nav_view(self):
        response = self.client.get('/bins/bin/map/nav/')
        self.assertEqual(response.status_code, 200)

    def test_get_bin_nav_arrive(self):
        response = self.client.get('/bins/bin/map/arrive/')
        self.assertEqual(response.status_code, 200)
