import multireplacer from '../../dsl/multireplacer';

const C = '([bcdgjklmnprstvxzčďľňřśšťž])';
const V = '([aeiouyęěǫ])';
// "do", "iz", "na", "nad", "nedo", "o", "ob", "ob", "obez", "od", "po", "pod", "prě", "prěd", "pri", "pro", "raz", "de", "s", "so", "su", "u", "v", "vo", "voz", "vy", "za",

// adjective adverb conjunction determiner interjection morpheme multiword term noun numeral particle phrase postposition preposition pronoun verb

export default () =>
  multireplacer
    .named('Protoslavic → Interslavic')
    .rule('Ignore case', (r) => r.lowerCase())

    .rule('Ambigious reconstruction', (r) => r.regexp(/(\([a-z]\))/, ["$1", ""]))
    .rule('Ambigious reconstruction brackets cleanup', (r) => r.regexp(/(\(|\))/, [""]))

    .section('Time Reversal')
    .rule('-kti i -gti', (r) => r.regexp(/ťi$/, ["kti", "gti"]))
    .rule('epenthetic l', (r) => r.regexp(/([pbmv])ľ/, ["$1ľ", "$1j"]))
    .section('Adjectives')
    .rule(
        'Full and short adjectives',
        (r) => r.regexp(/(ъ|ь)$/, ['$1jь'])
        (p) => p.morphologyTags('Adjective')
    )
    .rule('DJ', (r) => r.regexp(/ď/, ["đ"]))
    .rule('TJ', (r) => r.regexp(/ť/, ["ć"]))
    .rule('DZ', (r) => r.regexp(/dz/, ["z"]))
    .rule('ždž', (r) => r.regexp(/ždž/, ["žd"]))
    .rule('DL', (r) => r.regexp(/dl/, ["l"]))
    .rule('initial vowels', (r) => r.regexp(/^([aeęě])/, ["j$1"]))
    .rule('Initial Big Yus', (r) => r.regexp(/^ǫ/, ["vų"]))
    .rule('Anti-Hiatus Big Yus', (r) => r.regexp(/{V}ǫ/, ["$1vų"]))
    .rule('initial j', (r) => r.regexp(/^jь{C}/, ['i$1']))
    .section('liquid metathesis')
    .rule('initial oRT', (r) => r.regexp(/^o([lr]){C}/, ['$1å$2', '$1a$2', '$1o$2']))
    .rule('CoRC', (r) => r.regexp(/{C}o([lr]){C}/, ['$1$2å$3']))
    .rule('CeRC', (r) => r.regexp(/{C}e([lr]){C}/, ['$1$2ě$3']))

    .section('Yers')
    .rule('Classify Yers', (r) => r.classifyYers())
    .section('Tense Yer')
    .rule('lьje', (r) => r.regexp(/lьj/, ["ĺj"]))
    .rule('nьje', (r) => r.regexp(/nьj/, ["ńj"]))
    .rule('rьje', (r) => r.regexp(/rьj/, ["ŕj"]))
    .rule('Ending Front Tense Yer', (r) => r.regexp(/[Ьь]jь$/, ["i"]))
    .rule('Ending Back Tense Yer', (r) => r.regexp(/[Ъъ]jь$/, ["y"]))
    .rule('Otherwise, Front Tense Yer', (r) => r.regexp(/[Ьь]j/, ["ij"]))
    .rule('Otherwise, Back Tense Yer', (r) => r.regexp(/[Ъъ]j/, ["yj"]))
    .rule('CъlC and CьlC', (r) => r.regexp(/{C}[ЪЬъь]l{C}/, ['$1ȯl$2']))
    .rule('CъrC', (r) => r.regexp(/{C}[Ъъ]r{C}/, ['$1r$2']))
    .rule('CьrC', (r) => r.regexp(/{C}[Ьь]r{C}/, ['$1ŕ$2']))
    .rule('rь', (r) => r.regexp(/rь/, ["ŕ"]))
    .rule('tь', (r) => r.regexp(/tь/, ["ť"]))
    .rule('dь', (r) => r.regexp(/dь/, ["ď"]))
    .rule('sь', (r) => r.regexp(/sь/, ["ś"]))
    .rule('zь', (r) => r.regexp(/zь/, ["ź"]))
    .rule('mekko L', (r) => r.regexp(/(ľ|lь)/, ["lj"]))
    .rule('mekko N', (r) => r.regexp(/(nь|ň)/, ["nj"]))
    .rule('Fall of Weak Yers', (r) => r.regexp(/[ьъ]/, [""]))

    .rule('Strong Front Yer', (r) => r.regexp(/Ь/, ["ė"]))
    .rule('Strong Back Yer', (r) => r.regexp(/Ъ/, ["ȯ"]))

    .section('Orthography')
    .rule('Big Yus', (r) => r.regexp(/ǫ/, ["ų"]))
    .rule('H', (r) => r.regexp(/x/, ["h"]))
    .rule('RJ', (r) => r.regexp(/ř/, ["rj"]))
    .rule('final RJ', (r) => r.regexp(/rj$/, ["ŕ"]))
    //.rule('tьje', (r) => r.regexp(/tьj{V}\b/, ["ťj$1"]))
    //.rule('dьje', (r) => r.regexp(/dьj{V}\b/, ["ďj$1"]))
    //.rule('sьje', (r) => r.regexp(/sьj{V}\b/, ["śj$1"]))
    //.rule('zьje', (r) => r.regexp(/zьj{V}\b/, ["źj$1"]))

    .rule('Restore case', (r) => r.restoreCase())
    .build();
