from django.test import SimpleTestCase
from django.urls import reverse, resolve
from unittest.mock import patch

from .forms import SourceTextInputForm
from .views import (
    translate,
    check_results,
    translation_direction,
    google_trans,
    microsoft_trans,
    aws_trans,
)


class TestUrls(SimpleTestCase):

    def test_root_url_redirect(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)

    def test_input_page_url(self):
        response = self.client.get(reverse("input"))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)

    def test_output_page_url(self):
        response = self.client.get(reverse("output"))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)


class TestViews(SimpleTestCase):

    def test_input_page_correct_view_used(self):
        response = self.client.get(reverse("input"))
        self.assertEqual(response.resolver_match.func, translate)
        self.assertNotEqual(response.resolver_match.func, check_results)

    def test_output_page_correct_view_used(self):
        response = self.client.get(reverse("output"))
        self.assertEqual(response.resolver_match.func, translate)
        self.assertNotEqual(response.resolver_match.func, check_results)


class TestForms(SimpleTestCase):

    def test_input_form_valid_data(self):
        form = SourceTextInputForm(
            data={
                "direction": "Ja>En",
                "source_text": "ゼルダは任天堂のコンピュータゲームシリーズ。",
            }
        )
        self.assertTrue(form.is_valid())

    def test_input_form_no_data(self):
        form = SourceTextInputForm(data={})
        self.assertFalse(form.is_valid())
        # There should be one error for each item of missing data
        self.assertEqual(len(form.errors), 2)


class TestHelperMethods(SimpleTestCase):

    def setUp(self):
        self.source = "ゼルダは任天堂のコンピュータゲームシリーズ。"
        self.src_lang = "ja"
        self.tar_lang = "en"
        self.direction1 = "Ja>En"
        self.direction2 = "En>Ja"
        google = google_trans(self.source, self.src_lang, self.tar_lang)
        microsoft = microsoft_trans(self.source, self.src_lang, self.tar_lang)
        aws = aws_trans(self.source, self.src_lang, self.tar_lang)
        self.results = [google, microsoft, aws]

    def test_check_results(self):
        checked_results = check_results(self.results)
        self.assertTrue(len(checked_results) == 3)

    def test_translation_direction(self):
        src_lang, tar_lang = translation_direction(self.direction1)
        self.assertEqual(src_lang, "ja")
        self.assertEqual(tar_lang, "en")
        src_lang, tar_lang = translation_direction(self.direction2)
        self.assertEqual(src_lang, "en")
        self.assertEqual(tar_lang, "ja")

"""
To do:

Shouldn't access external API directly in test code.
Should use mock instead.
https://stackoverflow.com/questions/32433585/django-avoid-http-api-calls-while-testing-from-django-views
"""

"""
class TestTranslateView(SimpleTestCase):

    @patch(aws_trans)
    @patch(microsoft_trans)
    @patch(google_trans)
    def test_translate_view_with_data(self, mock_get):
        response = self.client.post(
            reverse("input"),
            data={
                "direction": "Ja>En",
                "source_text": "ゼルダは任天堂のコンピュータゲームシリーズ。",
            },
        )
"""
