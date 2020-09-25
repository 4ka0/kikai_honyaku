from django.http import HttpResponse
from django.shortcuts import render

import os
import requests
import uuid
import json
import boto3
from googletrans import Translator

# To use environment variables
from environs import Env
env = Env()
env.read_env()


def home(request):
    return render(request, "input.html")


def translate(request):
    """
    Method to obtain translation results from Google, Microsoft, and AWS
    """

    # Get source text (from textbox having name "source" in input.html)
    source = request.GET["source"]

    # Get source and target languages
    # (from radio buttons having name "translation_direction" in input.html)
    direction = request.GET["translation_direction"]
    source_lang, target_lang = translation_direction(direction)

    # Get translation results
    google_result = google_translation(source, source_lang, target_lang)
    micro_result = microsoft_translation(source, source_lang, target_lang)
    aws_result = aws_translation(source, source_lang, target_lang)

    # If any result is empty, replace with something more readable
    results = [google_result, micro_result, aws_result]
    results = check_results(results)

    return render(request, "output.html", {"source": source,
                                           "google_result": results[0],
                                           "microsoft_result": results[1],
                                           "aws_result": results[2],},)


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


def google_translation(source, source_lang, target_lang):
    """
    Uses the googletrans library to access Google Translate
    https://pypi.org/project/googletrans/
    """
    translator = Translator()
    result = translator.translate(
        source, src=source_lang, dest=target_lang
    )
    return result.text


def microsoft_translation(source, source_lang, target_lang):
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


def aws_translation(source, source_lang, target_lang):
    """
    Uses own AWS subscription key to access Amazon Translate, under which
    machine translation is available under a freemium model for 2M chars free
    per month for a period of one year.
    """
    translate = boto3.client(service_name="translate", use_ssl=True)
    result = translate.translate_text(
        Text=source,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang,
    )
    return result.get("TranslatedText")
