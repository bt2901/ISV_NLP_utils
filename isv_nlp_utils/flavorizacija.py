
CS_FLAVOR = {
    "VERB":
    {
        "infn": (-2, 't'),
        # "1per+sing": (-1, 'u'),
        "2per+sing": {'aješ': 'áš', 'iš': 'íš'},
        "3per+sing": {'aje': 'á', 'i': 'í'},
        "1per+plur": {'ajemo': 'áme', 'imo': 'íme'},
        "2per+plur": {'ajete': 'áte', 'ite': 'íte'},
        "3per+plur": {'jųt': 'jí', 'ųt': 'ou', 'ęt': "í"},
    },
    "NOUN":
    {
        "gent+sing+masc": (-1, "e"),
        "accs+sing+masc": (-1, "e"),
        "gent+plur+masc": (-2, "ů"),
        "datv+plur+masc": (-2, "ům"),
        "accs+plur+masc": (-2, "e"),
        "loct+plur+masc": (-2, "ech"),
        "ablt+sing+femn": (-3, "ou"),
        "datv+plur+femn": (-2, "ám"),
        "ablt+sing+neut": (-2, "em"),
        "datv+plur+neut": (-2, "ům"),
        "loct+plur+neut": (-2, "ech")
    },
    "ADVB": {"ADVB": (-1, 'ě')},
    "ADJF":
    {
        "nomn+plur+femn": (-1, "é"),
        "accs+plur+femn": (-1, "é"),
        "nomn+sing+neut": (-1, "é"),
        "accs+sing+neut": (-1, "é"),
        "nomn+plur+neut": (-1, "á"),
        "accs+plur+neut": (-1, "á"),

        "accs+sing+femn": (-1, "ou"),
        "ablt+sing+femn": (-1, "ou"),
        "loct+sing+masc": (-2, "ém"),
        "loct+sing+neut": (-2, "ém"),
        "loct+sing+femn": (-2, "é"),
        "datv+sing+femn": (-2, "é"),
        "gent+sing+femn": (-2, "é"),

        "accs+plur+masc": (-2, "é"),
        "loct+plur": (-2, "ých"),
        "datv+plur": (-2, "ých"),
        "ablt+plur": (-3, "ými"),
    }
}


PL_FLAVOR = {
    "VERB":
    {
        "infn": (-2, 'Ч'),
        "1per+sing": (-1, 'ę'),
        "3per+plur": (-2, 'ą'),
    },
    "NOUN":
    {
        "loct+sing+masc": (-1, "ě"),
        "accs+sing+femn": (-1, "ę"),
    },
    "ADVB": {"ADVB": (-1, 'e')},
    "ADJF":
    {
        "nomn+plur+femn": (-1, "ie"),
        "accs+plur+femn": (-1, "ie"),
        "nomn+plur+neut": (-1, "ie"),
        "accs+plur+neut": (-1, "ie"),

        "accs+sing+femn": (-1, "ą"),
        "ablt+sing+femn": (-1, "ą"),

        "loct+sing+femn": (-2, "ej"),
        "datv+sing+femn": (-2, "ej"),
        "gent+sing+femn": (-2, "ej"),

        "accs+plur+masc": (-2, "ych"),
        "loct+plur": (-2, "ych"),
        "datv+plur": (-2, "ych"),
    }
}


SR_FLAVOR = {
    "VERB":
    {
    },
    "NOUN":
    {
        "nomn+plur+masc": (-1, "ovi"),
        "gent+plur+masc": (None, "a"),
        # TODO: https://fastlanguagemastery.com/learn-foreign-languages/serbian-language/serbian-cases-of-nouns/
    },
    "ADJF":
    {

        "nomn+sing+masc": {"ny": "an"},
        "gent+sing+masc": (-1, ""),
        "accs+sing+masc+anim": (-1, ""),
        "datv+sing+masc": (-1, ""),
        "loct+sing+masc": (-1, ""),

        "gent+sing+femn": (-2, "e"),
        "ablt+sing+femn": (-2, "om"),

        "loct+plur": (-2, "im"),
        "ablt+plur": (-3, "im"),
    }
}


RU_FLAVOR = {
    "VERB":
    {
        "infn": (-1, 'ь'),
        "3per+sing": (None, 't'),
    },
    "NOUN":
    {
        "loct+sing+masc": (-1, "ě"),
    },
    "ADJF":
    {
        "nomn+sing+femn": (None, "ja"),
        "nomn+sing+neut": (None, "ě"),
        "nomn+sing+masc": (None, "j"),

        "accs+sing+femn": (None, "ju"),
        "accs+sing+neut": (None, "ě"),
        "accs+sing+masc+anim": (None, ""),
        "accs+sing+masc+inan": (None, "j"),

        # "accs+plur": (None, "iě"),
        "nomn+plur": (-1, "ые"),
        "accs+plur+neut": (-1, "ые"),
        # "accs+plur+femn+anim": (-1, "ых"),
        # "accs+plur+femn+inan": (-1, "ые"),
        # "accs+plur+masc+anim": (-1, "ых"),
        # "accs+plur+masc+inan": (-1, "ые"),
    }
}


# no j/й/ь support
lat_alphabet = "abcčdeěfghijklmnoprsštuvyzžęųćåńľŕ"
cyr_alphabet = "абцчдеєфгхијклмнопрсштувызжяучанлр"
lat2cyr_trans = str.maketrans(lat_alphabet, cyr_alphabet)
pol_alphabet = "abcčdeěfghijklmnoprsštuwyzżęąconlr"
lat2pol_trans = str.maketrans(lat_alphabet, pol_alphabet)


def srb_letter_change(word):
    word = word.replace('ć', "ћ").replace('dž', "ђ").replace("ę", "е")
    word = word.translate(lat2cyr_trans)

    return word.replace('ы', "и").replace('нј', "њ").replace('лј', "љ")


def pol_letter_change(word):
    word = word.translate(lat2pol_trans)
    return (
        word
        .replace('č', "cz").replace('š', "sz")
        .replace('rj', "rz").replace('rě', "rze").replace('ri', "rzy")
        .replace('ě', "ie")
        .replace('Ч', "ć")
        .replace('lj', "л").replace('l', "ł").replace("л", "l").replace('łę', "lę")
        .replace('nj', "ni").replace('wj', "wi")
        .replace('ci', "cy")
        .replace('ji', "i")
        .replace('dż', "dz")
    )


def cz_letter_change(word):
    return (
        word
        .replace('ę', "ě")
        .replace('ų', "u")
        .replace('šč', "št")
        .replace('rje', "ří")
        .replace('rj', "ř")
        .replace('rě', "ře")
        .replace('ri', "ři")
        .replace('đ', "z")
        .replace('å', "a")
        .replace('h', "ch")
        .replace('g', "h")
        .replace('ć', "c")
        .replace('kě', "ce")
        .replace('gě', "ze")
        .replace('lě', "le")
        .replace('sě', "se")
        .replace('hě', "še")
        .replace('cě', "ce")
        .replace('zě', "ze")
        .replace('nju', "ni")
        .replace('nj', "ň")
        .replace('tje', "tí")
        .replace('dje', "dí")
        .replace('lju', "li")
        .replace('ču', "či")
        .replace('cu', "ci")
        .replace('žu', "ži")
        .replace('šu', "ši")
        .replace('řu', "ři")
        .replace('zu', "zi")
        .replace('ijejų', "í")
        .replace('ija', "e")
        .replace('ijų', "i")
        .replace('ij', "í")
    )


def rus_letter_change(word):
    word = word.replace("ń", "нь").replace("ľ", "ль")
    return (
        word.translate(lat2cyr_trans)
        .replace('ју', "ю").replace('ја', "я").replace('јо', "ё")
        .replace('ији', "ии")
        .replace('рј', "рь").replace('лј', "ль").replace('нј', "нь")
        .replace('ј', "й")
        .replace('йя', "я").replace('йе', "е")
        .replace('ья', "я").replace('ье', "е")
        .replace('дж', "жд")
    )
