import pymorphy2
import re

VERB_PREFIXES = [
    'do', 'iz', 'izpo', 'nad', 'na', 'ne', 'ob', 'odpo', 'od', 'o', 'prědpo',
    'pod', 'po', 'prě', 'pre', 'pri', 'pro', 'råzpro', 'razpro', 'råz', 'raz',
    'sȯ', 's', 'u', 'vȯ', 'vo', 'v', 'vȯz', 'voz', 'vy', 'za',
]

CYR_LETTER_SUBS = {
    "н": "њ", "л": "љ", "е": "є", "и": "ы"
}

SIMPLE_DIACR_SUBS = {
    'e': 'ě', 'c': 'č', 'z': 'ž', 's': 'š',
}

TOTAL_DIACR_SUBS = {
        'a': 'å', 'u': 'ų', 'e': ['ě', 'ę', 'ė'], 'č': 'ć', 'c': ['č', 'ć'],
        'o': 'ȯ',
        'n': 'ń', 'r': 'ŕ', 'l': 'ľ',
        'd': 'ď', 's': ['ś', 'š'], 't': 'ť', 'z': ['ź', 'ž'],
        # hack with dʒ = "đ"
        'ž': 'ʒ'  # đ ne funguje
}

ETM_DIACR_SUBS = {
        'a': 'å', 'u': 'ų', 'e': ['ě', 'ę', 'ė'], 'č': 'ć',
        'o': 'ȯ', 
        'n': 'ń', 'r': 'ŕ', 'l': 'ľ',
        'd': 'ď', 's': 'ś', 't': 'ť', 'z': 'ź',
        # hack with dʒ = "đ"
        'ž': 'ʒ'  # đ ne funguje
}


ALPHABET_LETTERS = {
    'lat': "abcdefghijklmnoprstuvyzěčšž",
    'cyr': "абвгдежзиклмнопрстуфхцчшыєјљњ",
    'etm': "abcdefghijklmnoprstuvyzåćčďėęěľńŕśšťųźžȯʒ",
}

ADDITIONAL_ETM_LETTERS = "åćďėęľńŕśťųźȯʒ"
DOWNGRADED_ETM_LETTERS = "ačdeelnrstuzož"

downgrade_diacritics = str.maketrans(ADDITIONAL_ETM_LETTERS, DOWNGRADED_ETM_LETTERS)


letters = "a-zа-яёěčžšåųćęđŕľńĺťďśźʒėȯђјљєњ"
alphanum = f"[0-9{letters}_]"

BASE_ISV_TOKEN_REGEX = re.compile(
    f'''(?:-|[^{letters}\\s"'""«»„“-]+|{alphanum}+(-?{alphanum}+)*)''',
    re.IGNORECASE | re.UNICODE
)

DISCORD_USERNAME_REGEX = re.compile(
    r'''@((.+?)#\d{4})''',
    re.IGNORECASE | re.UNICODE
)


# from collections import namedtuple
# _dummy = namedtuple('mock', 'dictionary')
# pymorphy2.units.DictionaryAnalyzer(_dummy(None))

DEFAULT_UNITS = [
    [
        pymorphy2.units.DictionaryAnalyzer()
    ],
    pymorphy2.units.KnownPrefixAnalyzer(known_prefixes=VERB_PREFIXES),
    [
        pymorphy2.units.UnknownPrefixAnalyzer(),
        pymorphy2.units.KnownSuffixAnalyzer()
    ]
]


def iterate_over_text(paragraph, extended=False):
    delimiters = BASE_ISV_TOKEN_REGEX.finditer(paragraph)
    for delim in delimiters:
        if any(c.isalpha() for c in delim.group()):
            token = delim.group()
            if extended:
                yield delim
            else:
                yield token


def create_analyzers_for_every_alphabet(path="C:\\dev\\pymorphy2-dicts\\"):

    std_morph = pymorphy2.MorphAnalyzer(
        path+"out_isv_lat",
        units=DEFAULT_UNITS,
        char_substitutes=SIMPLE_DIACR_SUBS
    )

    etm_morph = pymorphy2.MorphAnalyzer(
        path+"out_isv_etm",
        units=DEFAULT_UNITS,
        char_substitutes=ETM_DIACR_SUBS
    )

    cyr_morph = pymorphy2.MorphAnalyzer(
        path+"out_isv_cyr",
        units=DEFAULT_UNITS,
        char_substitutes=CYR_LETTER_SUBS
    )
    abecedas = {"lat": std_morph, "etm": etm_morph, "cyr": cyr_morph}
    return abecedas
