from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import home, translate


class TestInputPage(SimpleTestCase):

    # Test to see if the url exists
    def test_input_page_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    # Test to see if the correct view is being used
    def test_input_page_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    # Test to see if the correct template is being used
    def test_input_page_template(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html')


class TestTranslatePage(SimpleTestCase):

    # Test to see if the url exists
    def test_translate_page_status_code(self):
        path = "/translate/"
        csrf_token = "?csrfmiddlewaretoken=tIfyCpW09wEhijZY4Er1999ntE2WGxWcAsrak2zkOfIUag3gmh8eV1AxzUOlpsFR"
        direction = "&translation-direction=Ja%3EEn"
        source_text = "&source-text=ゼルダの伝説シリーズは任天堂が開発・発売しているコンピュータゲームシリーズ。"
        url = path + csrf_token + direction + source_text
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    """

    # Test to see if the correct view is being used
    def test_translate_page_view(self):
        response = self.client.get(reverse('translate'))
        self.assertEqual(response.status_code, 200)

    # Test to see if the correct template is being used
    def test_translate_page_template(self):
        response = self.client.get(reverse('translate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'translate.html')

    """

# use paramaterize to test the smaller helper functions
