from lexer import Lexer

def main():
    lexer = Lexer()
    tokens = lexer.emit_tokens("mem[6] < -15 and mem[12] = 0 --> forward;")
    for token in tokens:
        print(f'Got: {token}')

    lexemes = lexer.emit_lexemes("mem[6] < -15 and mem[12] = 0 --> forward;")
    for lexeme in lexemes:
        print(f'Got: {lexeme}')


if __name__ == "__main__":
    main()
