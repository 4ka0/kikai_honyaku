from django.test import SimpleTestCase
from django.urls import reverse, resolve

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


class TestTemplates(SimpleTestCase):
    def test_input_page_template(self):
        response = self.client.get(reverse("input"))
        self.assertTemplateUsed(response, "input.html")
        self.assertTemplateNotUsed(response, "output.html")

    """
    def test_output_page_template(self):
        response = self.client.get(reverse("output"))
        self.assertTemplateUsed(response, "output.html")
        self.assertTemplateNotUsed(response, "input.html")
    """


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


class TestTranslationEngines(SimpleTestCase):
    def setUp(self):
        self.source = "ゼルダは任天堂のコンピュータゲームシリーズ。"
        self.src_lang = "ja"
        self.tar_lang = "en"

    def test_google_trans(self):
        result = google_trans(self.source, self.src_lang, self.tar_lang)
        result = result.strip()
        self.assertTrue(result)

    def test_microsoft_trans(self):
        result = microsoft_trans(self.source, self.src_lang, self.tar_lang)
        result = result.strip()
        self.assertTrue(result)

    def test_aws_trans(self):
        result = aws_trans(self.source, self.src_lang, self.tar_lang)
        result = result.strip()
        self.assertTrue(result)


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
        self.assertTrue(checked_results[0], True)
        self.assertTrue(checked_results[1], True)
        self.assertTrue(checked_results[2], True)

    def test_translation_direction(self):
        src_lang, tar_lang = translation_direction(self.direction1)
        self.assertEqual(src_lang, "ja")
        self.assertEqual(tar_lang, "en")
        src_lang, tar_lang = translation_direction(self.direction2)
        self.assertEqual(src_lang, "en")
        self.assertEqual(tar_lang, "ja")


class TestTranslateView(SimpleTestCase):
    def test_translate_view_with_data:
        response = self.client.post(reverse("input"), data={"direction": "Ja>En",
                                                            "source_text": "ゼルダは任天堂のコンピュータゲームシリーズ。",})
        """ ... """



"""
To do:

Shouldn't access external API directly in test code.
Should use mock instead, apparently.
https://stackoverflow.com/questions/32433585/django-avoid-http-api-calls-while-testing-from-django-views
"""