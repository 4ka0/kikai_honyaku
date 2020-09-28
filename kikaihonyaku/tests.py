from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import home, translate


class TestUrls(SimpleTestCase):
    """
    Tests to see if the urls exist
    """

    def test_home_page_url(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_translate_page_url(self):
        path = "/translate/"
        csrf_token = "?csrfmiddlewaretoken=tIfyCpW09wEhijZY4Er1999ntE2WGxWcAsrak2zkOfIUag3gmh8eV1AxzUOlpsFR"
        direction = "&translation-direction=Ja%3EEn"
        source_text = "&source-text=ゼルダの伝説シリーズは任天堂が開発・発売しているコンピュータゲームシリーズ。"
        url = path + csrf_token + direction + source_text
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_translate_page_url_2(self):
        data = {
            'source-text': 'ゼルダの伝説シリーズは任天堂が開発・発売しているコンピュータゲームシリーズ。',
            'translation-direction': 'Ja>En'
        }
        response = self.client.get(reverse("translate"),params=data)
        self.assertEqual(response.status_code, 200)



class TestViews(SimpleTestCase):

    # Tests to see if the correct views are being used

    def test_translate_page_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    """
    def test_translate_page_view(self):
        response = self.client.get(reverse('translate'))
        self.assertEqual(response.status_code, 200)
    """

    # Tests to see if the correct templates are being used

    def test_home_page_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    """
    def test_translate_page_template(self):
        response = self.client.get(reverse('translate'))
        self.assertTemplateUsed(response, 'translate.html')
    """


# use paramaterize to test the smaller helper functions
