import pandas as pd
from razdel import tokenize
import re
import unicodedata
from string import punctuation

from natasha.record import Record

class AnnotatedToken(Record):
    __attributes__ = ['text', 'capitalization', 'space_after', 'features', 'POS', 'slovnik_pos', 'lemma', 'isv_id', 'genesis', 'is_processed']


def convert2MSPlus(thestring):
    # "e^" -> "ê"
    # 'z\u030C\u030C\u030C' -> 'ž\u030C\u030C'
    thestring = unicodedata.normalize(
        'NFKC',
        thestring
    )
    # TODO: do the same for upper case
    thestring = (
        thestring
        .replace("ň", "ń").replace("ĺ", "ľ")
        .replace("d\u0301", "ď").replace("t\u0301", "ť")
        .replace("l\u0301", "ľ").replace("n\u0301", "ń")
        .replace("ò", "ȯ").replace("è", "ė")
        .replace("ǉ", "lj").replace("ĳ", "ij").replace("ǌ", "nj").replace("t́", "ť").replace("d́", "ď")
    )
    return thestring

def compute_annotated_tokens(src, morph, slovnik):
    src = convert2MSPlus(src)
    tokens = list(tokenize(src))

    tokens_data = []

    for i, t in enumerate(tokens):
        if i + 1 < len(tokens):
            space_after = src[t.stop: tokens[i+1].start]
        else:
            space_after = ""
        cap = "title" if t.text.istitle() else "upper" if t.text.isupper() else False
        parses = morph.parse(t.text.replace("đ", "dʒ"))
        if parses:
            # TODO: HANDLE NON-DETERMINISM HERE
            # BECAUSE I CAN AND WHY NOT
            isv_lemma = parses[0].normal_form
            tag = parses[0].tag
            entry = slovnik[slovnik.isv == isv_lemma]
            pos = str(tag.POS)
            if len(entry):
                isv_id = entry.index[0]
                isv_genesis = entry.genesis.values[0]
                slovnik_pos = entry.partOfSpeech.values[0]
            else:
                isv_id = -1
                isv_genesis = ""
                slovnik_pos = ""
        else:
            tag = None
            pos = "PUNCT" if t.text in punctuation else "UNKNOWN"
            isv_lemma = None
            isv_id = -1
            isv_genesis = ""
            slovnik_pos = ""

        ann_token = AnnotatedToken(
            [t.text],
            cap, space_after,
            tag, pos, slovnik_pos, isv_lemma,
            isv_id, isv_genesis, False
        )
        tokens_data.append(ann_token)
    return tokens_data


if __name__ == "__main__":
    Src = "Kromě togo, kȯgda sědite v problematikě MS, v glåvě sę vam skladaje taky sistem kako maly domȯk iz kostȯk Lego. V mojej glåvě jest po tutom principu vȯznikla bogatějša forma MS, ktorų råboće, sam za sebę, nazyvajų srědnoslovjańsky. Čisty MS jest posvęćeny ljud́am i komunikaciji, zato trěbuje byti universaĺno råzumlivy tako mnogo, kako jest možno. Iz drugoj stråny bogatějši međuslovjańsky, teoretično upotrěblivy v literaturě ili pěsnjah, jest na tutčas glåvno za prijateljev językov. K drugym ljud́am on ne progovori, zatože on v sobě imaje bogat́stvo vsih slovjańskyh językov, a vśaky slovjańskojęzyčny člověk znaje jedino tų čęst́, ktorų v sobě imaje jegovy język."
    compute_annotated_tokens(Src)

