from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import translate
from .forms import SourceTextInputForm


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

    """
    def test_output_page_template(self):
        response = self.client.post(reverse("output"))
        self.assertTemplateUsed(response, "output.html")
    """

class TestForms(SimpleTestCase):

    def test_input_form_valid_data(self):
        form = SourceTextInputForm(data={
            "direction": "Ja>En",
            "source_text": "ゼルダの伝説シリーズは任天堂のコンピュータゲームシリーズ。"
        })
        self.assertTrue(form.is_valid())

    def test_input_form_no_data(self):
        form = SourceTextInputForm(data={})
        # This form contains no data and therefore should not be valid
        self.assertFalse(form.is_valid())
        # There should be one error for each item of missing data
        self.assertEquals(len(form.errors), 2)


# use paramaterize to test the smaller helper functions
