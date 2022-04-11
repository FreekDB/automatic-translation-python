from typing import List


class TranslateRequest:
    def __init__(self, source_texts: List[str], target_languages: List[str]):
        self.source_texts = source_texts
        self.target_languages = target_languages


class SourceTranslateResponse:
    def __init__(self, source_text: str, detected_source_language: str, translations: dict[str, str], errors: str):
        self.source_text = source_text
        self.detected_source_language = detected_source_language
        self.translations = translations
        self.errors = errors


class TranslateResponse:
    def __init__(self, data: List[SourceTranslateResponse]):
        self.data = data

    def to_json(self):
        json_data = []

        for source_translation in self.data:
            json_data.append(
                {
                    'sourceText': source_translation.source_text,
                    'detectedSourceLanguage': source_translation.detected_source_language,
                    'translations': source_translation.translations
                }
            )

        return json_data
