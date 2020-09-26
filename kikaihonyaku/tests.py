from django.test import SimpleTestCase

# URL tests
# test that the input and output pages are actually rendered with a 200 code
# being received

class TestURLs(SimpleTestCase):

    def test_input_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_output_page_status_code(self):
        # Build url to test including form-related data
        base_url = "/translate/"
        csrf_token = "?csrfmiddlewaretoken=tIfyCpW09wEhijZY4Er1999ntE2WGxWcAsrak2zkOfIUag3gmh8eV1AxzUOlpsFR"
        direction = "&translation-direction=Ja%3EEn"
        source_text = "&source-text=ゼルダの伝説シリーズは任天堂が開発・発売しているコンピュータゲームシリーズ。"
        url = base_url + csrf_token + direction + source_text
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

# use paramaterize to test the smaller helper functions
