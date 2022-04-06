from flask import Flask
from flask_restful import Api, Resource

# export GOOGLE_APPLICATION_CREDENTIALS='Test Google Cloud Translation-5cd266aa0073.json'
from google.cloud import translate_v2

flaskApp = Flask(__name__)
api = Api(flaskApp)


class AutomaticTranslation(Resource):
    def get(self):
        text = 'Arise'
        target = 'de'
        translate_client = translate_v2.Client()
        result = translate_client.translate(text, target_language=target)
        translation = result['translatedText']
        data = {'usedId': 246, 'name': 'Freek', 'city': 'Barcelona', 'arise': translation}
        return {'data': data}, 200


api.add_resource(AutomaticTranslation, '/translate')


if __name__ == '__main__':
    flaskApp.run()

