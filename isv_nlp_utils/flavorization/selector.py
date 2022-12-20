import lingua
lingua.isocode.IsoCode639_3

LANGS = [
    'bel', 'ukr', 'rue', 'rus', 'bos', 'hrv', 'srp', 'cnr', 'slv', 'bul', 'mkd', 'chu', 'wen', 'dsb', 'hsb', 'pol', 'szl', 'csb', 'pox', 'ces', 'czk', 'slk',
]

LANGS = [
    getattr(lingua.isocode.IsoCode639_3, l.upper())
    for l in LANGS
    if l.upper() in dir(lingua.isocode.IsoCode639_3)
]
print(LANGS)

detector = lingua.LanguageDetectorBuilder.from_iso_codes_639_3(*LANGS).build()


def get_conf(confs, lang):
    if lang not in confs:
        return 0
    the_sum = sum(dict(confs).values())
    return {k: v / the_sum for (k, v) in confs}[lang]

final = []
for token in tokens_data:
    w = token.text
    if len(w) > 1:
        scores = {}
        for cand in w:
            if cand:
                confs = detector.compute_language_confidence_values(cand)
                scores[cand] = get_conf(confs, LANG_OBJ)
        print(scores)
        final.append(max(scores, key=lambda x: scores[x]) + token.space_after)
    else:
        final.append(w[0] + token.space_after)

final = "".join(final)
final
