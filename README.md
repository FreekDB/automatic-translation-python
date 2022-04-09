# automatic-translation-python
A simple Python Flask application providing an API to Google Translation.

Example of a post request:

http://localhost:8080/translate


```json
{
    "sourceTexts": [
        "In de eerste regel staan wat mooie woorden.",
        "In the second line less translation is needed.",
        "Die dritte Zeile enthält andere Wörter."
    ],
    "targetLanguages": ["en", "hu"]
}
```


Response:


```json
{
    "data": [
        {
            "sourceText": "In de eerste regel staan wat mooie woorden.",
            "detectedSourceLanguage": "nl",
            "translations": {
                "en": "There are some nice words in the first line.",
                "hu": "Az első sorban van néhány szép szó."
            }
        },
        {
            "sourceText": "In the second line less translation is needed.",
            "detectedSourceLanguage": "en",
            "translations": {
                "en": "In the second line less translation is needed.",
                "hu": "A második sorban kevesebb fordításra van szükség."
            }
        },
        {
            "sourceText": "Die dritte Zeile enthält andere Wörter.",
            "detectedSourceLanguage": "de",
            "translations": {
                "en": "The third line contains other words.",
                "hu": "A harmadik sor más szavakat tartalmaz."
            }
        }
    ]
}
```


The Automatic Translation application can easily be extended to support for example DeepL and Microsoft Translate in the future. A short experiment has already been done with both translation providers, as can be seen in the code on this page: [EXTENDING.md](EXTENDING.md).
