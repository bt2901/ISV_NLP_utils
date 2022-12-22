import regex


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



def check_constraint(token, constraint):
    for single_constraint in constraint:
        if single_constraint[0] == "partOfSpeech":
            allowed_pos = [p.strip() for p in single_constraint[1].split(",")]
            #if len(allowed_pos) > 1:
            #    print(allowed_pos)
            #    print(token.slovnik_pos)
            #    print(all(p not in token.slovnik_pos for p in allowed_pos), any(p in token.slovnik_pos  for p in allowed_pos))

            # TODO: https://github.com/medzuslovjansky/razumlivost/blob/main/src/customization/predicates/PartOfSpeechFilter.ts
            if all(p not in token.slovnik_pos for p in allowed_pos):
                return False
        if single_constraint[0] == "genesis":
            this_negated = "!" in single_constraint[1]
            this_approximate = "?" in single_constraint[1]
            this_value = single_constraint[1].strip("?!")
            unknown_genesis = (token.genesis != token.genesis) or not token.genesis
            
            does_apply = (token.genesis == this_value) or (this_approximate and unknown_genesis)
            
            #if not unknown_genesis:
            #    print(single_constraint)
            #    print(token.genesis)
            # does_apply and this_negated -> False
            # not does_apply and not this_negated -> False
            if does_apply == this_negated:
                return False
    return True


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
            if len(rule) == 3:
                mapping = rule[2]
                constraint = [("", "")]
            else:
                mapping = rule[2]
                constraint = rule[3]
                constraint = [(con_type, con_cond.strip("'")) for con_type, con_cond in constraint.asList()]

            for (a, b) in mapping:
                for i in range(len(tokens_data)):
                    is_constraint_satisfied = check_constraint(tokens_data[i], constraint)
                    if not is_constraint_satisfied:
                        continue
                    for j, w in enumerate(tokens_data[i].text):
                        tokens_data[i].text[j] = w.replace(a, b)

        if typ == "r.regexp":
            if len(rule) == 4:
                name, typ, pattern, subst = rule
                constraint = [("", "")]
            else:
                name, typ, pattern, subst, constraint = rule
                constraint = [(con_type, con_cond.strip("'")) for con_type, con_cond in constraint.asList()]
            subst = subst.asList()
            subst = [s.replace("$", "\\").strip("'") for s in subst]
            pattern = pattern.replace("\x08", "$")
            try:
                compiled = regex.compile(pattern)
            except regex.error as e:
                print(e, "in", name)
                continue
            for i in range(len(tokens_data)):
                is_constraint_satisfied = check_constraint(tokens_data[i], constraint)
                if not is_constraint_satisfied:
                    continue

                prev_words = list(tokens_data[i].text)
                candidates = []
                for j, w in enumerate(tokens_data[i].text):
                    for one_subst in subst:
                        cand = compiled.sub(one_subst, w)
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

