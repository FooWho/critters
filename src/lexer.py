import re

class Lexer():

    patterns = {
        "T_MEMSIZE": r"MEMSIZE|mem\[0\]", 
        "T_DEFENSE": r"DEFENSE|mem\[1\]",
        "T_OFFENSE": r"OFFENSE|mem\[2\]",
        "T_SIZE": r"SIZE|mem\[3\]",
        "T_ENERGY": r"ENERGY|mem\[4\]",
        "T_PASS": r"PASS|mem\[5\]",
        "T_POSTURE": r"POSTURE|mem\[6\]",
        "T_COMM": r"-->",
        "T_ASSIGN": r":=",
        "T_LEQU": r"<=",
        "T_GEQU": r">=",
        "T_NEQU": r"!=",
        "T_MEM": r"\bmem\b",
        "T_WAIT": r"\bwait\b",
        "T_FORWARD":r"\bforward\b",
        "T_BACKWARD": r"\bbackward\b",
        "T_LEFT": r"\bleft\b",
        "T_RIGHT": r"\bright\b",
        "T_EAT": r"\beat\b",
        "T_ATTACK": r"\battack\b",
        "T_GROW": r"\bgrow\b",
        "T_BUD": r"\bbud\b",
        "T_SERVE": r"\bserve\b",
        "T_NEARBY": r"\bnearby\b",
        "T_AHEAD": r"\bahead\b",
        "T_RANDOM": r"\brandom\b",
        "T_SMELL": r"\bsmell\b",
        "T_AND": r"\band\b",
        "T_OR": r"\bor\b",
        "T_MOD": r"\bmod\b",
        "T_STAR": r"\*",
        "T_DIV": r"/",
        "T_PLUS": r"\+",
        "T_MINUS": r"\-",
        "T_LESS": r"<",
        "T_GREAT": r">",
        "T_EQU": r"=",
        "T_L_PAREN": r"\(",
        "T_R_PAREN": r"\)",
        "T_L_BRACKET": r"\[",
        "T_R_BRACKET": r"\]",
        "T_L_BRACE": r"\{",
        "T_R_BRACE": r"\}",
        "T_SEMICOLON": r";",
        "T_NUMBER": r"\d+"
    }

    def __init__(self):
        self.combined_pattern = "|".join([f'(?P<{name}>{pattern})' for name, pattern in self.patterns.items()])
        self.compiled_pattern = re.compile(self.combined_pattern)

    def emit_tokens(self, loc:str) -> list[str] :
        tokens = []
        for match in self.compiled_pattern.finditer(loc):
            tokens.append(match.lastgroup)
        return tokens

    
    def emit_lexemes(self, loc:str) -> list[str] :
        tokens = []
        matches = self.compiled_pattern.finditer(loc)
        return [match.group() for match in matches]



