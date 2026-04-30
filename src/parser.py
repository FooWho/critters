from __future__ import annotations
from typing import ClassVar, Iterable, Iterator
from schemas import ConditionCommandTuple, TokenLexeme, TermTuple, RelationTuple, FactorTuple, Token, CritterParseError

class ASTNode():
    _children: ClassVar[tuple[str, ...]] = ()
    
    def __iter__(self) -> Iterable[ASTNode]:
        for fieldName in self._children:
            value = getattr(self, fieldName, None)
            if isinstance(value, list):
                yield from (item for item in value 
                            if isinstance(item, ASTNode))
            elif isinstance(value, ASTNode):
                yield value

class Program(ASTNode):
    _children: ClassVar[tuple[str]] = ('rules',)

    def __init__(self, rules: list[Rule]|None = None) -> None:
        self.rules: list[Rule] = rules or []

    def addRule(self, rule: Rule|None = None, 
                conditionCommandTuple: ConditionCommandTuple|None = None) -> None:
        if rule and not conditionCommandTuple:
            self.rules.append(rule)
        elif not rule and conditionCommandTuple:
            self.rules.append(Rule(conditionCommandTuple))
        else:
            raise ValueError('Invalid arguments: Provide either a "rule" or both a'
                             ' "condition" and a "command".')
        

class Rule(ASTNode):
    _children: ClassVar[tuple[str, str]] = ('condition', 'command')
    
    def __init__(self, conditionCommandTuple: ConditionCommandTuple|None = None) -> None:
        self.condition: Condition
        self.command: Command
        if conditionCommandTuple:
            self.condition = conditionCommandTuple.condition
            self.command = conditionCommandTuple.command
        else:
            self.condition = Condition()
            self.command = Command() 

    def setRule(self, conditionCommandTuple: ConditionCommandTuple) -> None: 
        self.condition = conditionCommandTuple.condition
        self.command = conditionCommandTuple.command


class Condition(ASTNode):
    _children: ClassVar[tuple[str]] = ('conjunctions',)
    
    def __init__(self, conjunctions: list[Conjunction]|None = None) -> None:
        self.conjunctions: list[Conjunction] = conjunctions or []

    def addConjunction(self, conjunction: Conjunction) -> None:
        self.conjunctions.append(conjunction)


class Command(ASTNode):
    _children: ClassVar[tuple[str, str]] = ('updates', 'action')

    def __init__(self) -> None:
        self.updates: list[Update] = []
        self.action: Action


class Update(ASTNode):
    pass


class Action(ASTNode):
    pass

class Conjunction(ASTNode):
    _children: ClassVar[tuple[str]] = ('relations',)

    def __init(self, relations: list[Relation]|None = None) -> None:
        self.relations: list[Relation] = relations or []


class Relation(ASTNode):
    _children: ClassVar[tuple[str, str]] = ('leftExpression', 'rightExpression')

    def __init__(self, relationTuple: RelationTuple|None = None) -> None:
        self.leftExpression: Expression
        self.rightExpression: Expression
        self.relationalOperator: TokenLexeme

        if relationTuple:
            self.leftExpression = relationTuple.leftExpression
            self.rightExpression = relationTuple.rightExpression
            self.relationalOperator = relationTuple.relationalOperator
        else:
            self.leftExpression = Expression([])
            self.rightExpression = Expression([])
            self.relationalOperator = TokenLexeme('T_NONE', '')



class Expression(ASTNode):
    _children: ClassVar[tuple[str]] = ('terms',)

    def __init__(self, terms: list[TermTuple]|None = None) -> None:
        self.terms: list[TermTuple] = terms or []

        for term in self.terms[0:1]:
            if term.addOp:
                raise ValueError('First term must not have an addOp')
        for term in self.terms[1:]:
            if not term.addOp:
                raise ValueError('All joining terms must have an addOp.')       

    def __repr__(self) -> str:
        tmp: str = ''

        for term in self.terms[0:1]:
            tmp += str(term)
        for term in self.terms[1:]:
            tmp += term.addOp.lexeme
            tmp += str(term)

        return tmp
    
    def addTerm(self, term: TermTuple) -> None:
        if not self.terms:
            if term.addOp is not None:
                raise ValueError('First term must not have addOp')
        else:
            if term.addOp is None:
                raise ValueError('All joining terms must have an addOp')
        self.terms.append(term)
        

class Term(ASTNode):
    _children: ClassVar[tuple[str]] = ('factors',)

    def __init__(self, factors: list[FactorTuple]|None = None) -> None:
        self.factors:list[FactorTuple] = factors or []

        for factor in self.factors[0:1]:
            if factor.mulOp:
                raise ValueError('First factor must not have mulOp')
        for factor in self.factors[1:]:
            if not factor.mulOp:
                raise ValueError('All joining facotrs must have a mulOp')

    def __repr__(self) -> str:
        tmp:str = ''
        for factor in self.factors[0:1]:
            tmp += str(factor.factor)
        for factor in self.factors[1:]:
            tmp += factor.mulOp.lexeme
            tmp += str(factor.factor)

        return tmp


    def addFactor(self, factor: FactorTuple) -> None:
        if not self.factors:
            if factor.mulOp is not None:
                raise ValueError('First factor must not have mulOp')
        else:
            if factor.mulOp is None:
                raise ValueError('All joining factors must have a mulOp')
        self.factors.append(factor)
            


class Factor(ASTNode):
    _children: ClassVar[tuple[str, ...]] = ()

    def __init__(self, number: TokenLexeme|None = None) -> None:
        self.number: TokenLexeme = number or TokenLexeme('T_NONE', ' ')

    def __repr__(self) -> str:
        return self.number.lexeme


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

        while self.peek() is not None:
            program.addRule(self.parseRule())
            self.getToken()

        return program

    def parseRule(self) -> Rule:
        rule: Rule = Rule()
        condition: Condition
        command: Command

        self.eatWhitespace()
        condition = self.parseCondition()
        command = self.parseCommand()

        return rule
    
    def parseCondition(self) -> Condition:
        condition: Condition = Condition()
        conjunctions: list[Conjunction] = []
        conjunction: Conjunction = Conjunction()

        # A Condition may have a list of conjunctions, for now, we will assume 1 and fix later
        conjunction = self.parseConjunction()

        return condition
    
    
    def parseCommand(self) -> Command:
        command: Command = Command()


        return command
    
    def parseConjunction(self) -> Conjunction:
        conjunction: Conjunction = Conjunction()
        relation: Relation = Relation()

        # A Conjunction may have a list of relations,  for now assume one and fix later
        relation = self.parseRelation()

        return conjunction
    
    def parseRelation(self) -> Relation:
        relation: Relation = Relation()
        leftExpression: Expression
        rightExpression: Expression
        relOp: TokenLexeme

        leftExpression = self.parseExpression()

        print(f'leftExpression: {leftExpression}')


        return relation
    
    def parseExpression(self) -> Expression:
        expression: Expression = Expression()
        term: Term

        term = self.parseTerm()
        expression.addTerm(TermTuple(TokenLexeme('T_NONE', ''), term))

        return expression
    
    def parseTerm(self) -> Term:
        term: Term = Term()
        factor: Factor

        factor = self.parseFactor()
        term.addFactor(FactorTuple(None, factor))

        return term
    
    def parseFactor(self) -> Factor:
        factor: Factor
        number: TokenLexeme

        number = self.parseNumber()
        factor = Factor(number)

        return factor
    
    def parseNumber(self) -> TokenLexeme:
        token: Token|None
        tokenLexeme: TokenLexeme = TokenLexeme('T_NONE', '')

        token = self.peek()
        if not token or token.tokenType != 'T_NUMBER':
            raise CritterParseError("Error!")
        else:
            tokenLexeme = TokenLexeme(token.tokenType, token.lexeme)
        return tokenLexeme

    
    def eatWhitespace(self) -> None:
        token: Token|None = self.peek()

        while token and token.tokenType == 'T_WS':
            token = self.getToken()
            token = self.peek()
    





