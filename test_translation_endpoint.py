import unittest

from automatictranslationpython import TranslateRequest
from automatictranslationpython import TranslationEndpoint


class TestTranslationEndpoint(unittest.TestCase):
    def test_success(self):
        source_texts = ["Test source text."]
        translate_request = TranslateRequest(source_texts, ["en", "hu"])
        translate_client = MockGoogleTranslateClient()

        translate_response = TranslationEndpoint().handle_translate_request(translate_request, translate_client)

        self.assertEqual(f'en: {source_texts[0]}', translate_response['data'][0]['translations']['en'])


class MockGoogleTranslateClient:
    @staticmethod
    def translate(source_texts, target_language):
        return [
            {
                'input': source_texts[0],
                'detectedSourceLanguage': 'fr',
                'translatedText': f'{target_language}: {source_texts[0]}'
            }
        ]


if __name__ == '__main__':
    unittest.main()
