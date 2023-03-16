from django.test import TestCase, Client

# Create your tests here.

class TestNotLoggedIn(TestCase):
    # Test pages when user is not logged in
    def setUp(self):
        self.client = Client()

    def test_scanner(self):
        response = self.client.get('/scanner/')
        self.assertEqual(response.status_code, 302)

    def test_recycle_confirm(self):
        response = self.client.get('/scanner/recycle/confirm')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/scanner/recycle/confirm/', 301), ('/account/login/', 302)])


class TestLoggedIn(TestCase):
    # Test pages when user is logged in

    def setUp(self):
        self.client = Client()
        self.client.login(username='cameron', password='PopTest')

    def test_scanner_logged_in(self):
        response = self.client.get('/scanner/')
        self.assertEqual(response.status_code, 200)

    def test_recycle_confirm_logged_in(self):
        session = self.client.session
        session['valid'] = -1
        session.save()
        response = self.client.get('/scanner/recycle/confirm', follow=True)
        self.assertEqual(response.redirect_chain, [('/scanner/recycle/confirm/', 301), ('/', 302)])

    def test_recycle_confirm_valid_session(self):
        session = self.client.session
        session['valid'] = 1
        session['barcode'] = 500128584364
        session['newHome'] = 'XFI-LEC'
        session.save()
        response = self.client.get('/scanner/recycle/confirm', follow=True)
        self.assertEqual(response.redirect_chain, [('/scanner/recycle/confirm/', 301), ('/', 302)])
