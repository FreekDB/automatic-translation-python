import unittest

from typing import List

from data_classes import TranslateResponse
from translator import LanguageCleaner, Translator


class MockTranslator(Translator):
    def get_supported_languages(self) -> List[str]:
        return ['zh-CN', 'zh-TW', 'en', 'nl', 'fr', 'de', 'es', 'it']

    def translate_texts(self, source_texts: List[str], target_languages: List[str]) -> TranslateResponse:
        return TranslateResponse([])


class LanguageCleanerTest(unittest.TestCase):
    def test_strip_dialects(self):
        supported_languages = ['zh-cn', 'zh-tw', 'en', 'nl', 'fr', 'de', 'es', 'it']
        language_ranges_with_dialects = ['zh-cn', 'zh-tw', 'en-us,en-ca;q=0.8', 'nl-be', 'fr-ca', 'de-sw', 'es-me', 'it']
        translator = MockTranslator()

        language_cleaner = LanguageCleaner()

        self.assertEqual(supported_languages, language_cleaner.clean(translator.get_supported_languages(), translator))
        self.assertEqual(supported_languages, language_cleaner.clean(language_ranges_with_dialects, translator))

    def test_filter_languages(self):
        supported_languages = ['en', 'nl', 'fr', 'de', 'es', 'it']
        expected_languages = ['en', 'nl', 'fr', 'de', 'es', 'it', 'zh-tw']
        language_ranges_with_unsupported = supported_languages + ['vi;q=0.2', 'cy,yo;q=0.6', 'zu', 'zh-MO']
        translator = MockTranslator()

        language_cleaner = LanguageCleaner()

        self.assertEqual(expected_languages, language_cleaner.clean(language_ranges_with_unsupported, translator))
