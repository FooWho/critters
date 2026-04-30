import re
from typing import Iterator
from schemas import Token, TokenLexeme, CritterParseError

class Lexer():

    patterns = {
        'T_MEMSIZE': r'MEMSIZE|mem\[0\]', 
        'T_DEFENSE': r'DEFENSE|mem\[1\]',
        'T_OFFENSE': r'OFFENSE|mem\[2\]',
        'T_SIZE': r'SIZE|mem\[3\]',
        'T_ENERGY': r'ENERGY|mem\[4\]',
        'T_PASS': r'PASS|mem\[5\]',
        'T_POSTURE': r'POSTURE|mem\[6\]',
        'T_COMMENT': r'//.*',
        'T_COMM': r'-->',
        'T_ASSIGN': r':=',
        'T_LEQU': r'<=',
        'T_GEQU': r'>=',
        'T_NEQU': r'!=',
        'T_MEM': r'\bmem\b',
        'T_WAIT': r'\bwait\b',
        'T_FORWARD':r'\bforward\b',
        'T_BACKWARD': r'\bbackward\b',
        'T_LEFT': r'\bleft\b',
        'T_RIGHT': r'\bright\b',
        'T_EAT': r'\beat\b',
        'T_ATTACK': r'\battack\b',
        'T_GROW': r'\bgrow\b',
        'T_BUD': r'\bbud\b',
        'T_SERVE': r'\bserve\b',
        'T_NEARBY': r'\bnearby\b',
        'T_AHEAD': r'\bahead\b',
        'T_RANDOM': r'\brandom\b',
        'T_SMELL': r'\bsmell\b',
        'T_AND': r'\band\b',
        'T_OR': r'\bor\b',
        'T_MOD': r'\bmod\b',
        'T_STAR': r'\*',
        'T_DIV': r'/',
        'T_PLUS': r'\+',
        'T_MINUS': r'\-',
        'T_LESS': r'<',
        'T_GREAT': r'>',
        'T_EQU': r'=',
        'T_L_PAREN': r'\(',
        'T_R_PAREN': r'\)',
        'T_L_BRACKET': r'\[',
        'T_R_BRACKET': r'\]',
        'T_L_BRACE': r'\{',
        'T_R_BRACE': r'\}',
        'T_SEMICOLON': r';',
        'T_NUMBER': r'\d+',
        'T_WS': r'\s',
        'T_EOF': r'\Z',
        'T_MISMATCH': r'.*',
        'T_NONE': r''  
    }

    def __init__(self):
        self.combinedPattern = '|'.join([f'(?P<{name}>{pattern})' for name, pattern in self.patterns.items()])
        self.compiledPattern = re.compile(self.combinedPattern)

    def tokenize(self, code: str) -> Iterator[Token]:
        tokenType: str
        lexeme: str 
        lineNumber:int
        column: int
        lineStart: int
        tmp: str|None

        lineStart = 0
        lineNumber = 0
        for tc in self.compiledPattern.finditer(code):
            tmp = tc.lastgroup

            if tmp:
                tokenType = tmp
            else:
                tokenType = 'T_MISMATCH'

            lexeme = tc.group()
            column = tc.start() - lineStart

            if tokenType == 'T_WS':
                if '\n' in lexeme:
                    lineNumber += lexeme.count('\n')
                    lineStart = tc.end()
                continue
            elif tokenType == 'T_COMMENT':
                lineNumber += lexeme.count('\n')
                lineStart = tc.end()
            elif tokenType == 'T_MISMATCH':
                raise CritterParseError(f'Error parsing critter program. Read: "{lexeme}" at line {lineNumber} column {column}.')
            yield Token(tokenType, lexeme, lineNumber, column)


    def emitTokens(self, loc: str) -> list[str|None]:
        return [match.lastgroup for match in self.compiledPattern.finditer(loc)]
    
    def emitLexemes(self, loc: str) -> list[str]:
        return [match.group() for match in self.compiledPattern.finditer(loc)]
    
    def emitLexemeTokenPair(self, loc: str) -> list[TokenLexeme]:
        return [TokenLexeme(token.tokenType, token.lexeme) for token in self.tokenize(loc)]




