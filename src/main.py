import sys
from typing import Iterator
from lexer import Lexer, Token
from parser import Parser, Program, Rule, Condition, Command, Conjunction, Relation, Expression, Term, Factor
from schemas import ConditionCommandTuple, TokenLexeme

def main(args: list[str]):
    
    tokens: Iterator[Token]
    token: Token|None
    lexer: Lexer
    factor: Factor

    lexer = Lexer()
    tokens = lexer.tokenize("1 = 1 --> eat;")
    parser = Parser(tokens)

    token = parser.nextToken()
    while token is not None:
        print(f'The current token is: {parser.currentToken()}')
        print(f'{token}')
        token = parser.nextToken()



    program: Program = Program()
    rule: Rule = Rule()
    condition: Condition = Condition()
    command: Command = Command()
    conjunction: Conjunction = Conjunction()
    relation: Relation = Relation()
    leftExpression: Expression = Expression()
    rightExpression: Expression = Expression()
    term: Term
    factor: Factor


if __name__ == "__main__":
    main(sys.argv)
