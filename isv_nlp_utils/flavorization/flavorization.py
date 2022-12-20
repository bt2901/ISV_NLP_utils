from .parsing import parse_multireplacer_rules
from .tokenizer import compute_annotated_tokens
from .replacer import process_multireplacing, morphological_flavorise

from isv_nlp_utils import constants
from isv_nlp_utils.slovnik import get_slovnik
# from isv_translate import translate_sentence, postprocess_translation_details, prepare_parsing

if __name__ == "__main__":
    LANG = "ru"
    rules_struct = parse_multireplacer_rules(
        r"C:\dev\razumlivost\src\flavorizers\{}.ts".format(LANG)
    )
    Src = "Kromě togo, kȯgda sědite v problematikě MS, v glåvě sę vam skladaje taky sistem kako maly domȯk iz kostȯk Lego. V mojej glåvě jest po tutom principu vȯznikla bogatějša forma MS, ktorų råboće, sam za sebę, nazyvajų srědnoslovjańsky. Čisty MS jest posvęćeny ljud́am i komunikaciji, zato trěbuje byti universaĺno råzumlivy tako mnogo, kako jest možno. Iz drugoj stråny bogatějši međuslovjańsky, teoretično upotrěblivy v literaturě ili pěsnjah, jest na tutčas glåvno za prijateljev językov. K drugym ljud́am on ne progovori, zatože on v sobě imaje bogat́stvo vsih slovjańskyh językov, a vśaky slovjańskojęzyčny člověk znaje jedino tų čęst́, ktorų v sobě imaje jegovy język."

    slovnik = get_slovnik()
    slovnik = slovnik['words']

    morph = constants.create_analyzers_for_every_alphabet(r"C:\dev\ISV_data_gathering\\")['etm']
    tokens = compute_annotated_tokens(Src, morph, slovnik)

    from ast import literal_eval

    with open(r"C:\dev\razumlivost\src\flavorizers\morpho_{}.txt".format(LANG), "r", encoding="utf8") as f:
        flavor_rules = literal_eval(f.read())
    ju = True

    morphological_flavorise(tokens, morph, flavor_rules, ju)

    res = process_multireplacing(tokens, rules_struct)
    print(res)

