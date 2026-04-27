import sys
from typing import Iterator
from lexer import Lexer, CritterParseError, Token

def main(args: list[str]):
    lexer = Lexer()
    #tokens = lexer.emitTokens("Blah Blah")
    #for token in tokens:
    #    print(f'Got: {token}')

    #lexemes = lexer.emitLexemes("Blah Blah")
    #for lexeme in lexemes:
    #    print(f'Got: {lexeme}')

    tokens: Iterator[Token] = iter([])
    with open('program.ctl') as f:
        source: str = f.read()
        tokens = lexer.tokenize(source)
    try:
        for token in tokens:
            print(f'{token}')
    except CritterParseError as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)
