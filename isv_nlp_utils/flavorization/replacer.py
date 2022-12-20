import re


def morphological_flavorise(tokens_data, morph, flavor_rules, ju):
    for i, token in enumerate(tokens_data):
        original = token.text[0]
        flavorised = flavorise(token.text[0].lower(), token.POS, morph, flavor_rules, ju=ju)
        if original != flavorised:
            print(original, flavorised)
            token.text[0] = flavorised
            # print(token)


def flavorise(word, golden_pos_tag, isv_morph, flavor, ju):
    if word in flavor["SPECIAL_CASES"]:
        return flavor["SPECIAL_CASES"][word]
    word = word.replace("đ", "dʒ")
    return __flavorise(word, golden_pos_tag, isv_morph, flavor, ju).replace("dʒ", "đ")

def __flavorise(word, golden_pos_tag, isv_morph, flavor, ju):
    if golden_pos_tag == "PNCT":
        return word
    if golden_pos_tag == "ADVB":
        variants = [
            v for v in isv_morph.parse(word)
            if v.tag.POS == "ADJF"
            and v.tag.number == "sing" and v.tag.gender == "neut" and v.tag.case == "nomn"
        ]
        if not variants:
            return word
    else:
        variants = [v for v in isv_morph.parse(word) if golden_pos_tag in v.tag]

    if not variants:
        return word

    if ju:
        if golden_pos_tag == "VERB" and all(v.tag.person == "1per" for v in variants):
            tags = variants[0].tag.grammemes  # no better way to choose
            new_tags = set(tags) - {'V-m'} | {'V-ju'}
            word = isv_morph.parse(word)[0].inflect(new_tags).word

    if golden_pos_tag == "ADJF":
        variants = [variants[0]]  # no better way to choose

    flavor_rules = flavor.get(golden_pos_tag, {})
    if golden_pos_tag == "ADVB":
        flavor_rules = {"ADJF": flavor_rules.get('ADVB', (None, ''))}

    for condition_plus, transform in flavor_rules.items():
        if condition_plus == "":
            is_match = True
        else:
            conditions_arr = condition_plus.split("+")
            is_match = all(
                all(cond in v.tag for cond in conditions_arr)
                for v in variants
            )
        if is_match:
            if isinstance(transform, tuple):
                suffix, addition = transform
                return word[:suffix] + addition
            if isinstance(transform, dict):
                for base, replacement in transform.items():
                    if word[-len(base):] == base:
                        return word[:-len(base)] + replacement

    return word




def process_multireplacing(tokens_data, rules): 
    for rule in rules:
        #print(rule)
        name, typ = rule[:2]
        if "lowerCase" in typ:
            for i in range(len(tokens_data)):
                for j, w in enumerate(tokens_data[i].text):
                    tokens_data[i].text[j] = w.lower()
        if "restoreCase" in typ:
            for i in range(len(tokens_data)):
                cap = tokens_data[i].capitalization
                if cap:
                    for j, w in enumerate(tokens_data[i].text):
                        tokens_data[i].text[j] = w.title() if cap == "title" else w.upper()
            
        if typ == "r.map":
            for (a, b) in rule[2:]:
                for i in range(len(tokens_data)):
                    for j, w in enumerate(tokens_data[i].text):
                        tokens_data[i].text[j] = w.replace(a, b)
        if typ == "r.regexp":
            if len(rule) == 4:
                name, typ, pattern, subst = rule
                constraint = ("", "")
            else:
                name, typ, pattern, subst, constraint = rule
                constraint = constraint.asList()
                constraint[1:] = [c.strip("'") for c in constraint[1:]]
            subst = subst.asList()
            subst = [s.replace("$", "\\").strip("'") for s in subst]
            pattern = pattern.replace("\x08", "$")
            try:
                re.compile(pattern)
            except re.error as e:
                print(e, "in", name)
                continue
            for i in range(len(tokens_data)):
                if constraint[0] == "partOfSpeech":
                    if constraint[1] not in tokens_data[i].slovnik_pos:
                        continue
                prev_words = list(tokens_data[i].text)
                candidates = []
                for j, w in enumerate(tokens_data[i].text):
                    for one_subst in subst:
                        cand = re.sub(pattern, one_subst, w)
                        candidates.append(cand)
                tokens_data[i].text = list(set(candidates))
                if len(tokens_data[i].text) > len(prev_words):
                    if tokens_data[i].POS == "PUNCT":
                            raise NameError
                    print(name)
                    print(prev_words, " => ", tokens_data[i].text)
            # print(name, len(candidates), len(set(candidates)))
            # words = choice(candidates)


    final = "".join([
        (t.text[0] if len(t.text) == 1 else f"[{'|'.join(t.text)}]") + t.space_after
        for t in tokens_data
    ])
    return final

