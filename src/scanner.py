import re
from enum import StrEnum

class Terminals(StrEnum):
    T_COMM = r"-->"
    T_ASSIGN = r":="
    T_LEQU = r"<="
    T_GEQU = r">="
    T_NEQU = r"!="
    T_MEM = r"\bmem\b"
    T_WAIT = r"\bwait\b"
    T_FORWARD = r"\bforward\b"
    T_BACKWARD = r"\bbackward\b"
    T_LEFT = r"\bleft\b"
    T_RIGHT = r"\bright\b"
    T_EAT = r"\beat\b"
    T_ATTACK = r"\battack\b"
    T_GROW = r"\bgrow\b"
    T_BUD = r"\bbud\b"
    T_SERVE = r"\bserve\b"
    T_NEARBY = r"\bnearby\b"
    T_AHEAD = r"\bahead\b"
    T_RANDOM = r"\brandom\b"
    T_SMELL = r"\bsmell\b"
    T_AND = r"\band\b"
    T_OR = r"\bor\b"
    T_MOD = r"\bmod\b"
    T_STAR = r"\*"
    T_DIV = r"/"
    T_PLUS = r"\+"
    T_MINUS = r"\-"
    T_LESS = r"<"
    T_GREAT = r">"
    T_EQU = r"="
    T_L_PAREN = r"\("
    T_R_PAREN = r"\)"
    T_L_BRACKET = r"\["
    T_R_BRACKET = r"\]"
    T_L_BRACE = r"\{"
    T_R_BRACE = r"\}"
    T_SEMICOLON = r";"
    T_NUMBER = r"\d+"

class StringTerminals(StrEnum):
    T_COMM = "-->"
    T_ASSIGN = ":="
    T_LEQU = "<="
    T_GEQU = ">="
    T_NEQU = "!="
    T_MEM = "mem"
    T_WAIT = "wait"
    T_FORWARD = "forward"
    T_BACKWARD = "backward"
    T_LEFT = "left"
    T_RIGHT = "bright"
    T_EAT = "beat"
    T_ATTACK = "attack"
    T_GROW = "grow"
    T_BUD = "bud"
    T_SERVE = "serve"
    T_NEARBY = "nearby"
    T_AHEAD = "ahead"
    T_RANDOM = "random"
    T_SMELL = "smell"
    T_AND = "and"
    T_OR = "or"
    T_MOD = "mod"
    T_STAR = "*"
    T_DIV = "/"
    T_PLUS = "+"
    T_MINUS = "-"
    T_LESS = "<"
    T_GREAT = ">"
    T_EQU = "="
    T_L_PAREN = "("
    T_R_PAREN = ")"
    T_L_BRACKET = "["
    T_R_BRACKET = "]"
    T_L_BRACE = "{"
    T_R_BRACE = "}"
    T_SEMICOLON = ";"

class Scanner():

    def __init__(self):
        self.pattern = "|".join([t.value for t in Terminals])
        self.compiled_pattern = re.compile(self.pattern)
        self.pattern_dictionary = {}
        for st in StringTerminals:
            self.pattern_dictionary.update({st.value: st.name})

    def emit_tokens(self, loc:str) -> list[str] :
        tokens = []
        matches = self.compiled_pattern.finditer(loc)
        while (match := next(matches, None)) is not None:
            lexeme = match.group()
            if lexeme.isdigit():
                lexeme = "T_NUMBER"
                tokens.append(lexeme)
            else:
                tokens.append(self.pattern_dictionary.get(lexeme))
        return tokens
    
    def emit_lexemes(self, loc:str) -> list[str] :
        tokens = []
        matches = self.compiled_pattern.finditer(loc)
        return [match.group() for match in matches]



