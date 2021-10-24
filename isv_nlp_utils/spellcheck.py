from .constants import BASE_ISV_TOKEN_REGEX, ALPHABET_LETTERS, iterate_over_text, create_analyzers_for_every_alphabet, downgrade_diacritics
from .normalizacija import transliterate_cyr2lat, fix_text, convert2MSPlus


def dodavaj_bukvy(word, etm_morph):
    corrected = [f.word for f in etm_morph.parse(word)]
    if len(set(corrected)) == 1:
        return corrected[0]
    if len(set(corrected)) == 0:
        return word + "/?"
    return "/".join(set(corrected))


def edit_distance_1(letters, word):
    """
    Compute all strings that are one edit away from `word` using only
    the letters in the corpus
    Args:
        word (str): The word for which to calculate the edit distance
    Returns:
        set: The set of strings that are edit distance one from the \
        provided word
    """

    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def create_set_if_known(word, morph):
    razbor = morph.parse(word)
    if not razbor:
        return set()
    diacr_form = razbor[0].word
    if morph.word_is_known(diacr_form):
        return {diacr_form}
    return set()


def spellcheck_text(paragraph, abeceda_name, morph, strict=True):
    delimiters = BASE_ISV_TOKEN_REGEX.finditer(paragraph)
    proposed_corrections = []
    token_candidates_cache = {}
    for delim in delimiters:
        token = delim.group().lower()
        is_word = any(c.isalpha() for c in delim.group())
        is_correct = None
        corrected = None
        confident_correction = None

        if is_word:
            is_correct = True
            candidates = set([f.word for f in morph.parse(token)])
            is_known = morph.word_is_known(token)
            if candidates != {token} or not is_known:
                is_correct = False
            # what if adding diacritics is not enough to make word's spelling known?
            # for starters, we will not suggest diacritic-fixed variant as the solution
            if strict and not is_known:
                candidates = set()
            # secondly, let's attempt to fix that token
            if not is_known:
                for fixer_name, fixer_func in fix_text.items():
                    changed_token = fixer_func(token)
                    if changed_token not in token_candidates_cache:
                        local_candidates = set()
                        local_candidates |= create_set_if_known(changed_token, morph)
                        for near_token in edit_distance_1(ALPHABET_LETTERS[abeceda_name], changed_token):
                            local_candidates |= create_set_if_known(near_token, morph)
                        token_candidates_cache[changed_token] = local_candidates
                    candidates |= token_candidates_cache[changed_token]
            if len(set(candidates)) >= 1:
                corrected = "/".join(set(candidates))

        markup = "" if is_correct or not is_word else "^" * len(token)
        if corrected and corrected != token:
            proposed_corrections.append(corrected)
            confident_correction = corrected
            markup = str(len(proposed_corrections))
        span_data = (delim.start(), delim.end(), markup)
        yield span_data, confident_correction


def perform_spellcheck(text, abeceda_name, selected_morph):
    text = convert2MSPlus(text)
    if abeceda_name == "lat":
        text = text.translate(downgrade_diacritics)
    data = list(spellcheck_text(text, abeceda_name, selected_morph))
    spans = [entry[0] for entry in data if entry[0][2]]
    proposed_corrections = [entry[1] for entry in data if entry[1]]
    return text, spans, proposed_corrections

