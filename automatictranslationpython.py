from typing import List

from flask import Flask, request
from flask_restful import Api, Resource

from google.cloud import translate_v2
from google.cloud.translate_v2.client import Client


flaskApp = Flask(__name__)
api = Api(flaskApp)


class AutomaticTranslation(Resource):
    @staticmethod
    def get():
        request_data = request.get_json()
        translate_request = TranslateRequest(request_data['sourceTexts'], request_data['targetLanguages'])
        translate_client = translate_v2.Client()

        translate_response = TranslationEndpoint.handle_translate_request(translate_request, translate_client)

        return translate_response, 200


class TranslateRequest:
    def __init__(self, source_texts: List[str], target_languages: List[str]):
        self.source_texts = source_texts
        self.target_languages = target_languages


class TranslationEndpoint:
    @staticmethod
    def handle_translate_request(translate_request: TranslateRequest, translate_client: Client):
        detected_source_languages = {}
        translations = {}

        for target_language in translate_request.target_languages:
            translations_by_language = translate_client.translate(translate_request.source_texts, target_language)

            for translation_by_language in translations_by_language:
                source_text = translation_by_language['input']
                detected_source_languages[source_text] = translation_by_language['detectedSourceLanguage']
                if source_text not in translations:
                    translations[source_text] = {}
                translations_for_source = translations.get(source_text)
                translations_for_source[target_language] = translation_by_language['translatedText']

        data = []

        for source_text in translate_request.source_texts:
            data.append(
                {
                    'sourceText': source_text,
                    'detectedSourceLanguage': detected_source_languages[source_text],
                    'translations': translations[source_text]
                }
            )

        return {'data': data}


api.add_resource(AutomaticTranslation, '/translate')


if __name__ == '__main__':
    flaskApp.run()
