from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import translate


class TestUrls(SimpleTestCase):

    def test_input_page_url(self):
        response = self.client.post(reverse("input"))
        self.assertEqual(response.status_code, 200)

    def test_output_page_url(self):
        response = self.client.post(reverse("output"))
        self.assertEqual(response.status_code, 200)


class TestViews(SimpleTestCase):

    # Tests to see if the correct templates are being used

    def test_input_page_template(self):
        response = self.client.post(reverse("input"))
        self.assertTemplateUsed(response, "input.html")

    def test_output_page_template(self):
        response = self.client.post(reverse("output"))
        self.assertTemplateUsed(response, "output.html")




# use paramaterize to test the smaller helper functions
