from django.shortcuts import render
import os, uuid, json

import requests
import boto3
from googletrans import Translator
from environs import Env

from .forms import SourceTextInputForm


# Environment variables
env = Env()
env.read_env()


def translate(request):

    # If the form has been populated
    if request.method == "POST":

        form = SourceTextInputForm(request.POST)

        if form.is_valid():

            # Get form data
            direction = form.cleaned_data["direction"]
            src_txt = form.cleaned_data["source_text"]

            # Determine source and target languages
            src_lang, tar_lang = translation_direction(direction)

            # Get translation results
            google = google_trans(src_txt, src_lang, tar_lang)
            microsoft = microsoft_trans(src_txt, src_lang, tar_lang)
            aws = aws_trans(src_txt, src_lang, tar_lang)

            # If any result is empty, replace with something more readable
            results = [google, microsoft, aws]
            results = check_results(results)

            return render(
                request,
                "output.html",
                {
                    "src_txt": src_txt,
                    "google": results[0],
                    "microsoft": results[1],
                    "aws": results[2],
                },
            )

    # If a blank form is to be displayed
    else:
        form = SourceTextInputForm()

    return render(request, "input.html", {"form": form})


def check_results(results):
    for elem in results:
        if not elem.strip():
            elem = "Not available."
    return results


def translation_direction(direction):
    if direction == "Ja>En":
        return "ja", "en"
    else:
        return "en", "ja"


def google_trans(source, source_lang, target_lang):
    """
    Uses the googletrans library to access Google Translate
    https://pypi.org/project/googletrans/
    """
    translator = Translator()
    result = translator.translate(source, src=source_lang, dest=target_lang)
    return result.text


def microsoft_trans(source, source_lang, target_lang):
    """
    Uses own azure subscription key to access Microsoft Translator, under which
    machine translation is available under a freemium model for 2M chars free
    per month for a period of one year.
    """

    # Set up
    AZURE_SUBSCRIPTION_KEY = env.str("AZURE_SUBSCRIPTION_KEY")
    azure_endpoint = "https://api.cognitive.microsofttranslator.com"
    path = "/translate?api-version=3.0"
    params = f"&from={source_lang}&to={target_lang}"

    # Build request
    constructed_url = azure_endpoint + path + params
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SUBSCRIPTION_KEY,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }
    body = [{"text": source}]
    request = requests.post(constructed_url, headers=headers, json=body)

    # Extract translation from response
    response = request.json()
    json_response = json.dumps(response)
    response_list = json.loads(json_response)
    response_dict = response_list[0]
    result = response_dict["translations"][0]["text"]

    return result


def aws_trans(source, source_lang, target_lang):
    """
    Uses own AWS subscription key to access Amazon Translate, under which
    machine translation is available under a freemium model for 2M chars free
    per month for a period of one year.
    """

    translate = boto3.client(
        service_name="translate",
        region_name="eu-west-2",
        use_ssl=True,
        aws_access_key_id=env.str("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=env.str("AWS_SECRET_ACCESS_KEY")
     )

    result = translate.translate_text(
        Text=source,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang,
    )

    return result.get("TranslatedText")
