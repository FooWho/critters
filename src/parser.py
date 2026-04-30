from __future__ import annotations
from typing import ClassVar, Iterable, Iterator
from schemas import Token, CritterParseError, TokenLexeme
from ASTNode import Program, Rule, Condition, Command, Conjunction, Relation, Expression, Term, Factor




class Parser():
    def __init__(self, tokens: Iterator[Token]) -> None:
        self.tokens: Iterator[Token] = tokens
        self.current: Token|None = next(tokens, None)

    def getToken(self) -> Token|None:
        token: Token|None = self.current
        self.current = next(self.tokens, None)
        return token
    
    def peek(self) -> Token|None:
        return self.current
    
    def parseProgram(self) -> Program:
        program: Program = Program()

        token = self.getToken()

        while token :
            program.addRule(self.parseRule(token))
            self.getToken()

        return program

    def parseRule(self, token: Token) -> Rule:
        rule: Rule = Rule()
        condition: Condition
        command: Command

        #self.eatWhitespace()
        condition = self.parseCondition(token)
        command = self.parseCommand()

        return rule
    
    def parseCondition(self, token: Token) -> Condition:
        condition: Condition = Condition()
        conjunctions: list[Conjunction] = []
        conjunction: Conjunction = Conjunction()

        # A Condition may have a list of conjunctions, for now, we will assume 1 and fix later
        conjunction = self.parseConjunction(token)

        return condition
    
    
    def parseCommand(self) -> Command:
        command: Command = Command()


        return command
    
    def parseConjunction(self, token: Token) -> Conjunction:
        conjunction: Conjunction = Conjunction()
        relation: Relation = Relation()

        # A Conjunction may have a list of relations,  for now assume one and fix later
        relation = self.parseRelation(token)

        print(f'{str(relation)}')

        return conjunction
    
    def parseRelation(self, token: Token) -> Relation:
        leftExpression: Expression
        relOp: TokenLexeme
        rightExpression: Expression

        leftExpression = self.parseExpression(token)
        nextToken: Token|None = self.getToken()
        if nextToken:
            token = nextToken
        else:
            raise CritterParseError('Error: Exprected relational operator in expression, but got "None"')
        relOp = TokenLexeme(token.tokenType, token.lexeme)
        nextToken = self.getToken()
        if nextToken:
            token = nextToken
        else:
            raise CritterParseError('Error: Exprected relational operator in expression, but got "None"')
        rightExpression = self.parseExpression(token)     


        return Relation(leftExpression, rightExpression, relOp)
    
    def parseExpression(self, token: Token) -> Expression:
        expression: Expression = Expression()
        term: Term

        term = self.parseTerm(token)
        expression.addTerm(term)

        return expression
    
    def parseTerm(self, token: Token) -> Term:
        term: Term = Term()
        addOp: TokenLexeme = TokenLexeme('T_NONE', '')
        factor: Factor

        if token.tokenType == 'T_ADDOP':
            addOp = TokenLexeme(token.tokenType, token.lexeme)
            tmpToken = self.getToken()
            if tmpToken:
                token = tmpToken
        factor = self.parseFactor(token)
        term.addFactor(factor)
        return term
    
    def parseFactor(self, token: Token) -> Factor:
        number: Factor
        mulOp: TokenLexeme

        factor = Factor(self.parseNumber(token))
        return factor
    
    def parseNumber(self, token: Token) -> TokenLexeme:

        if token.tokenType != 'T_NUMBER':
            raise CritterParseError('Error!')
        else:
            tokenLexeme = TokenLexeme(token.tokenType, token.lexeme)
        return tokenLexeme

    
    def eatWhitespace(self) -> None:
        token: Token|None = self.peek()

        while token and token.tokenType == 'T_WS':
            token = self.getToken()
            token = self.peek()
    





