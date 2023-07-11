from pyparsing import Group, Opt, Literal, Word, quoted_string, Suppress
import pyparsing

L = pyparsing.Literal
S = Suppress
QS = quoted_string.setParseAction(pyparsing.removeQuotes)


def build_parser():

    chars = pyparsing.unicode.alphas

    DICT_ENTRY = (
        (Word(chars) | "'’'")+ 
        L(":").suppress() + 
        L("'").suppress() + 
        Opt(Word(chars), default="") + 
        L("'").suppress() + 
        Opt(L(",")).suppress()
    )

    MAP_DESC = Group(
        S("{") + 
        pyparsing.OneOrMore(
            pyparsing.Group(DICT_ENTRY)
        )("map") + 
        S("}")
    )

    RULE_SPECIAL =  L("(r) => r.lowerCase()") | L("(r) => r.restoreCase()") | L("(r) => r.classifyYers()")
    RULE_REGEX = S("(r)") + S("=>") + "r.regexp" + S("(/") + ... + S("/") + S(",") + S('[') + Group(pyparsing.OneOrMore(QS + Opt(",").suppress())) + S(']') + S(")")
    RULE_MAP =   S("(r)") + S("=>") + "r.map" + S("(") + MAP_DESC + S(")")
    ONE_PREDICATE = (S("p.") + Group(Word(chars) + S("(") + QS + S(")"))) | S("p")

    CONSTRAINT = S("(p)") + S("=>") + (
        ONE_PREDICATE + Opt(pyparsing.OneOrMore(
            S(".and") + S("(") + ONE_PREDICATE + S(")")
        ))
    ) + Opt(",").suppress()

    rule_content = QS + S(",") + (RULE_REGEX | RULE_MAP | RULE_SPECIAL) + Opt(",").suppress() + Opt(Group(CONSTRAINT)) + Opt(",").suppress()

    rule_expr = pyparsing.nestedExpr( '(', ')', content=rule_content)


    element = (
        Group(Suppress(".rule") + S("(") + rule_content + S(")"))("rule") | 
        Group(Literal(".named") + S("(") + QS  + S(")"))("named") | 
        Group(Literal(".section") + S("(") + QS  + S(")"))("section")
    )

    parser = S("multireplacer") + pyparsing.ZeroOrMore(element) + L(".build();")

    return parser


def parse_multireplacer_rules(file_path, parser=None):
    CONST_RULE = S("const") + Word(pyparsing.alphanums) + S("=") + QS + Opt(";").suppress()

    with open(file_path, "r", encoding="utf8") as f:
        RULES = f.read().replace("t́", "ť").replace("d́", "ď")
    
    declared_constants = {}
    for i, line in enumerate(RULES.split("\n")):
        if "const" in line:
            k, v = CONST_RULE.parseString(line)
            declared_constants[k] = v

        if "multireplacer" in line and "import" not in line:
            break
    RULES = "\n".join(RULES.split("\n")[i:])

    RULES = "\n".join(l for l in RULES.split("\n") if not l.strip().startswith("//"))

    if not parser:
        parser = build_parser()
    return parser.parseString(RULES), declared_constants


if __name__ == "__main__":

    LANG = "ru"
    rules_struct = parse_multireplacer_rules(
        r"C:\dev\razumlivost\src\flavorizers\{}.ts".format(LANG)
    )
