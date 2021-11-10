
# this test does not use pytest because of some esoteric interaction between
# pytest and pymorphy2
# @pytest.mark.parametrize(
#    'base_text,expected', [
# import pytest

from isv_nlp_utils.normalizacija import normalize_and_simple_spellcheck
from isv_nlp_utils.spellcheck import perform_spellcheck
from isv_nlp_utils.constants import create_analyzers_for_every_alphabet

TEST_DATA_1 = [
        (
            'nakonec MS imaje uråvńje kako i vśaky drugy język',
            'nakonec MS imaje uråvńje kako i vśaky drugy język'
        ), (
            'Uvidimo čto budųt pisati na svojej veb-stranici',
            'Uvidimo čto bųdųt pisati na svojej veb-strånici'
        ), (
            'Desętok ljudij kto hcxe kritiku bude vzęti rolju. Toj kto piše vysxe grexsxek nezx slov, ne bude vzeti',  # noqa: E501
            'desętok ljudij kto hće kritiku bųde vzęti roljų. toj kto piše vyše grěšek než slov, ne bųde vzęti'  # noqa: E501
        )
]


def test_fixer(base_text, expected):
    # fixed = normalize_and_simple_spellcheck()
    abecedas = create_analyzers_for_every_alphabet()
    best_orthography, fixed, mean_score = normalize_and_simple_spellcheck(base_text, abecedas)
    if fixed.lower() != expected.lower():
        print(best_orthography, mean_score)
        print(fixed)
        print(expected)


def test_spellcheck():
    text = "zajmliov"
    perform_spellcheck(text, 'lat')


def test_homonyms():
    text = "zajmliov"
    perform_spellcheck(text, 'std')


if __name__ == "__main__":
    for base_text, expected in TEST_DATA_1:
        test_fixer(base_text, expected)
    test_spellcheck()
    test_homonyms()
