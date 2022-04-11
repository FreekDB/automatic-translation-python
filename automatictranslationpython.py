from flask import Flask, request
from flask_restful import Api, Resource

from google.cloud import translate_v2
from google.cloud.translate_v2.client import Client

from data_classes import TranslateRequest
from translator import GoogleTranslator


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


class TranslationEndpoint:
    @staticmethod
    def handle_translate_request(translate_request: TranslateRequest, translate_client: Client):
        translator = GoogleTranslator(translate_client)
        data = translator.translate_texts(translate_request.source_texts, translate_request.target_languages)

        return {'data': data.to_json()}


api.add_resource(AutomaticTranslation, '/translate')


if __name__ == '__main__':
    flaskApp.run()
