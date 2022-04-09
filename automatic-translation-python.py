from flask import Flask, request
from flask_restful import Api, Resource
from collections import namedtuple

# export GOOGLE_APPLICATION_CREDENTIALS='Test Google Cloud Translation-5cd266aa0073.json'
from google.cloud import translate_v2

flaskApp = Flask(__name__)
api = Api(flaskApp)


class AutomaticTranslation(Resource):
    @staticmethod
    def get():
        request_data = request.get_json()
        translate_request = namedtuple('TranslateRequest', request_data.keys())(*request_data.values())

        detected_source_languages = {}
        translations = {}

        for target_language in translate_request.targetLanguages:
            translate_client = translate_v2.Client()
            translations_by_language = translate_client.translate(translate_request.sourceTexts, target_language)

            for source_result in translations_by_language:
                source_text = source_result['input']
                detected_source_languages[source_text] = source_result['detectedSourceLanguage']
                if source_text not in translations:
                    translations[source_text] = {}
                translations_for_source = translations.get(source_text)
                translations_for_source[target_language] = source_result['translatedText']

        data = []

        for source_text in translate_request.sourceTexts:
            data.append(
                {
                    'sourceText': source_text,
                    'detectedSourceLanguage': detected_source_languages[source_text],
                    'translations': translations[source_text]
                }
            )

        return {'data': data}, 200


api.add_resource(AutomaticTranslation, '/translate')

if __name__ == '__main__':
    flaskApp.run()
