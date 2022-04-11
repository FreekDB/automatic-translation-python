import unittest

from automatic_translation_python import TranslationEndpoint, TranslateRequest


class TestTranslationEndpoint(unittest.TestCase):
    def test_success(self):
        source_texts = ['Test source text.']
        translate_request = TranslateRequest(source_texts, ['en', 'hu'])
        translate_client = MockGoogleTranslateClient()

        translate_response = TranslationEndpoint().handle_translate_request(translate_request, translate_client)

        translate_block = translate_response['data'][0]
        self.assertEqual(source_texts[0], translate_block['sourceText'])
        self.assertEqual('fr', translate_block['detectedSourceLanguage'])
        self.assertEqual(f'en: {source_texts[0]}', translate_block['translations']['en'])


class MockGoogleTranslateClient:
    def translate(self, values, target_language):
        return [
            {
                'input': values[0],
                'detectedSourceLanguage': 'fr',
                'translatedText': f'{target_language}: {values[0]}'
            }
        ]


if __name__ == '__main__':
    unittest.main()
