from __future__ import annotations
from typing import ClassVar, Iterable
from schemas import ConditionCommandTuple, TokenLexeme, TermTuple, RelationTuple

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
        self.rules: list[Rule]
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
        self.conjunctions: list[Conjunction]
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
    pass


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

    def __init__(self, terms: list[Term]|None = None) -> None:
        self.terms: list[Term] = []
        if terms is not None:
            self.terms = terms



class Term(ASTNode):
    _children: ClassVar[tuple[str, str]] = ('term', 'addop')

    def __init__(self, term: TermTuple|None = None) -> None:
        self.term: Term
        self.addop: TokenLexeme
        if term is not None:
            self.term = term.term
            self.addop = term.addOp


