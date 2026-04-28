from __future__ import annotations
from typing import ClassVar, Iterable, Iterator
from schemas import ConditionCommandTuple, TokenLexeme, TermTuple, RelationTuple, FactorTuple, Token

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
        self.rules: list[Rule] = []
        if rules is not None:
            self.rules = rules
        else:
            self.rules = []

    def addRule(self, rule: Rule|None = None, 
                conditionCommandTuple: ConditionCommandTuple|None = None) -> None:
        if rule is not None and conditionCommandTuple is None:
            self.rules.append(rule)
        elif rule is None and conditionCommandTuple is not None:
            self.rules.append(Rule(conditionCommandTuple))
        else:
            raise ValueError('Invalid arguments: Provide either a "rule" or both a'
                             ' "condition" and a "command".')
        

class Rule(ASTNode):
    _children: ClassVar[tuple[str, str]] = ('condition', 'command')
    
    def __init__(self, conditionCommandTuple: ConditionCommandTuple|None = None) -> None:
        self.condition: Condition
        self.command: Command
        if conditionCommandTuple is not None:
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
        self.conjunctions: list[Conjunction] = []
        if conjunctions is not None:
            self.conjunctions = conjunctions
        else:
            self.conjunctions = []

    def addConjunction(self, conjunction: Conjunction) -> None:
        self.conjunctions.append(conjunction)


class Command(ASTNode):
    _children: ClassVar[tuple[str, str]] = ('updates', 'action')

    def __init__(self) -> None:
        self.updates: list[Update] = []
        self.action: Action = Action()


class Update(ASTNode):
    pass


class Action(ASTNode):
    pass

class Conjunction(ASTNode):
    _children: ClassVar[tuple[str]] = ('relations',)

    def __init(self, relations: list[Relation]|None = None) -> None:
        self.relations: list[Relation] = []
        if relations is not None:
            self.relations = relations

class Relation(ASTNode):
    _children: ClassVar[tuple[str, str]] = ('leftExpression', 'rightExpression')

    def __init__(self, relationTuple: RelationTuple|None = None) -> None:
        self.leftExpression: Expression|None = None
        self.rightExpression: Expression|None = None
        self.relationalOperator: TokenLexeme|None = None

        if relationTuple is not None:
            self.leftExpression = relationTuple.leftExpression
            self.rightExpression = relationTuple.rightExpression
            self.relationalOperator = relationTuple.relationalOperator


class Expression(ASTNode):
    _children: ClassVar[tuple[str]] = ('terms',)

    def __init__(self, terms: list[TermTuple]|None = None) -> None:
        self.terms: list[TermTuple] = []
        if terms is not None:
            if terms[0].addOp is not None:
                raise ValueError('First term must not have addOp')
            for term in terms[1:]:
                if term.addOp is None:
                    raise ValueError('All joining terms must have an addOp.')
            self.terms = terms
    
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
        self.factors:list[FactorTuple] = []
        if factors is not None:
            if factors[0].mulOp is not None:
                raise ValueError('First factor must not have mulOp')
            for factor in factors[1:]:
                if factor.mulOp is None:
                    raise ValueError('All joining facotrs must have a mulOp')
            self.factors = factors

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

    def __init__(self, number: TokenLexeme|None) -> None:
        self.number: TokenLexeme|None = number











def parseRelation(token: Token, tokens: Iterator[Token]) -> Relation:
    relation: Relation = Relation()
    leftExpression: Expression = Expression()
    rightExpression: Expression = Expression()
    rel: TokenLexeme

    leftExpression = parseExpression(token, tokens)

    return relation

def parseExpression(token: Token, tokens: Iterator[Token]) -> Expression:
    expression: Expression = Expression()

    return expression


class Parser():
    def __init__(self, tokens: Iterator[Token]) -> None:
        self.tokens: Iterator[Token] = tokens
        self.token:Token|None = None
        self.token = self.nextToken()
      
    def nextToken(self) -> Token|None:
        self.token = next(self.tokens, None)
        return self.token
    
    def currentToken(self) -> Token|None:
        return self.token
    
    def parseProgram(self) -> Program:
        program: Program = Program()
        token: Token|None = self.currentToken()

        while token is not None:
            program.addRule(self.parseRule())

        return program

    def parseRule(self) -> Rule:
        rule: Rule = Rule()
        condition: Condition
        command: Command

        #condition = parseCondition()

        return rule
    
    def parseCondition(self) -> Condition:
        condition: Condition = Condition()
        conjunctions: list[Conjunction] = []
        conjunction: Conjunction = Conjunction()

        # A Condition may have a list of conjunctions, for now, we will assume 1 and fix later
        #conjunction = parseConjunction()

        return condition
    
    def parseConjunction(token: Token, tokens: Iterator[Token]) -> Conjunction:
    conjunction: Conjunction = Conjunction()
    relation: Relation = Relation()

    # A Conjunction may have a list of relations,  for now assume one and fix later
    relation = parseRelation(token, tokens)

    return conjunction
    






