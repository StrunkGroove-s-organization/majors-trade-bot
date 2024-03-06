from django.test import TestCase, Client


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')


class ProfitableLinksViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_profitable_links(self):
        response = self.client.get('profitable-links/')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profit_links.html')