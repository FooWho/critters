from scanner import Scanner

def main():
    my_scanner = Scanner()
    tokens = my_scanner.emit_tokens("ahead[3] < -15 and ahead[1] = 0 --> forward;")
    for token in tokens:
        print(f'Got: {token}')

    lexemes = my_scanner.emit_lexemes("ahead[3] < -15 and ahead[1] = 0 --> forward;")
    for lexeme in lexemes:
        print(f'Got: {lexeme}')


if __name__ == "__main__":
    main()
