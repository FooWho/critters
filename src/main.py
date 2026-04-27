import sys
from lexer import Lexer

def main(args: list[str]):
    lexer = Lexer()
    #tokens = lexer.emitTokens("Blah Blah")
    #for token in tokens:
    #    print(f'Got: {token}')

    #lexemes = lexer.emitLexemes("Blah Blah")
    #for lexeme in lexemes:
    #    print(f'Got: {lexeme}')

    with open('program.ctl') as f:
        tokens = lexer.tokenize(f.read())
    for token in tokens:
        print(f'{token}')


if __name__ == "__main__":
    main(sys.argv)
