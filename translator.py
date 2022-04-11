from typing import List

from google.cloud.translate_v2.client import Client

from data_classes import SourceTranslateResponse, TranslateResponse

CHINESE_DIALECTS = {
    'zh-hk': 'zh-tw',  # Map Hong Kong to Chinese (traditional)
    'zh-mo': 'zh-tw',  # Map Macau to Chinese (traditional)
    'zh-sg': 'zh-cn',  # Map Singapore to Chinese (simplified)
    'zh': 'zh-cn'  # Map general to Chinese (simplified)
}


class Translator:
    def process_language_exception(self, language: str) -> str:
        return CHINESE_DIALECTS.get(language, language)

    def is_language_supported(self, language: str) -> bool:
        return any(supported.casefold() == language.casefold() for supported in self.get_supported_languages())

    def get_supported_languages(self) -> List[str]:
        return []

    def translate_texts(self, source_texts: List[str], target_languages: List[str]) -> TranslateResponse:
        return TranslateResponse([])


FULLY_SUPPORTED_LANGUAGES = [
    'da',  # Danish
    'nl',  # Dutch
    'en',  # English
    'fi',  # Finnish
    'fr',  # French
    'de',  # German
    'hu',  # Hungarian
    'it',  # Italian
    'no',  # Norwegian
    'pl',  # Polish
    'pt',  # Portuguese
    'es',  # Spanish
    'sv'  # Swedish
]

ACCEPTED_CHINESE_DIALECTS = [
    'zh-CN',  # Chinese (simplified)
    'zh-TW'  # Chinese (traditional)
]

ACCEPTED_LANGUAGES = [
    'hr',  # Croatian
    'cs',  # Czech
    'et',  # Estonian
    'el',  # Greek
    'he',  # Hebrew
    'iw',  # Hebrew
    'is',  # Icelandic
    'ja',  # Japanese
    'ko',  # Korean
    'lv',  # Latvian
    'lt',  # Lithuanian
    'ro',  # Romanian
    'ru',  # Russian
    'sk',  # Slovak
    'sl',  # Slovenian
    'tr'  # Turkish
]

SUPPORTED_LANGUAGES = FULLY_SUPPORTED_LANGUAGES + ACCEPTED_CHINESE_DIALECTS + ACCEPTED_LANGUAGES


class GoogleTranslator(Translator):
    def __init__(self, translate_client: Client):
        self.translate_client = translate_client

    def get_supported_languages(self) -> List[str]:
        return SUPPORTED_LANGUAGES

    def translate_texts(self, source_texts: List[str], target_languages: List[str]) -> TranslateResponse:
        detected_source_languages = {}
        translations = {}

        for target_language in target_languages:
            translations_by_language = self.translate_client.translate(source_texts, target_language)

            for translation_by_language in translations_by_language:
                source_text = translation_by_language['input']
                detected_source_languages[source_text] = translation_by_language['detectedSourceLanguage']
                if source_text not in translations:
                    translations[source_text] = {}
                translations_for_source = translations.get(source_text)
                translations_for_source[target_language] = translation_by_language['translatedText']

        data = []

        for source_text in source_texts:
            data.append(SourceTranslateResponse(source_text, detected_source_languages[source_text],
                                                translations[source_text], ""))

        return TranslateResponse(data)


class LanguageCleaner:
    def strip_dialects(self, language: str) -> str:
        exception_languages = ['zh-cn', 'zh-tw']

        if language in exception_languages:
            return language
        else:
            return language.split('-')[0]

    def find_highest_supported_language(self, language_range: str, translator: Translator) -> str:
        languages = language_range.lower().split(",")

        clean_languages = []
        for language in languages:
            clean_language_split = language.split('=')
            clean_language = translator.process_language_exception(clean_language_split[0])
            clean_language = self.strip_dialects(clean_language)
            if translator.is_language_supported(clean_language):
                clean_languages.append(clean_language)

        if len(clean_languages) > 0:
            return clean_languages[0]
        else:
            return "en"

    def clean(self, target_language_ranges: List[str], translator: Translator) -> List[str]:
        languages = [self.find_highest_supported_language(language_range, translator)
                     for language_range in target_language_ranges]

        distinct_languages = []
        for language in languages:
            if language not in distinct_languages:
                distinct_languages.append(language)

        return distinct_languages
