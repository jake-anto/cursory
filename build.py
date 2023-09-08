import main

LANGS = [
    "bs",
    "da",
    "de",
    "el",
    "en",
    "es",
    "fi",
    "fr",
    "he",
    "ko",
    "no",
    "pl",
    "pt",
    "ru",
    "sco",
    "sv",
    "vi",
]

for language in LANGS:
    main.build(lang=language)
