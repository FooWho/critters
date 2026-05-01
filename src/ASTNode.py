from __future__ import annotations
from typing import ClassVar, Iterable
from schemas import TokenLexeme, FactorTuple, TermTuple

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

    def addRule(self, rule: Rule) -> None:
        self.rules.append(rule)

        

class Rule(ASTNode):
    _children: ClassVar[tuple[str, str]] = ('condition', 'command')
    
    def __init__(self, condition: Condition|None = None, command: Command|None = None) -> None:
        self.condition: Condition = condition or Condition()
        self.command: Command = command or Command()

    def setRule(self, condition: Condition, command: Command) -> None: 
        self.condition = condition
        self.command = command


class Condition(ASTNode):
    _children: ClassVar[tuple[str]] = ('conjunctions',)
    
    def __init__(self, conjunctions: list[Conjunction]|None = None) -> None:
        self.conjunctions: list[Conjunction] = conjunctions or []

    def addConjunction(self, conjunction: Conjunction) -> None:
        self.conjunctions.append(conjunction)


class Command(ASTNode):
    _children: ClassVar[tuple[str, str]] = ('updates', 'action')

    def __init__(self, updates: list[Update]|None = None, action: Action|None = None) -> None:
        self.updates: list[Update] = updates or []
        self.action: Action = action or Action()


# An update production is ultimately a "storage" instruction. The grammar defines it as: UPDATE => mem [ EXPR ] := EXPR
# The Update node will have a dst expression and a src expression. The interpretation will be to load the value
# of src into dst.
class Update(ASTNode):
    _children: ClassVar[tuple[str, str]] = ('dst', 'src')

    def __init__(self, dst: Expression|None = None, src: Expression|None = None) -> None:
        self.dst: Expression = dst or Expression()
        self.src: Expression = src or Expression()

class Action(ASTNode):
    pass

class Conjunction(ASTNode):
    _children: ClassVar[tuple[str]] = ('relations',)

    def __init(self, relations: list[Relation]|None = None) -> None:
        self.relations: list[Relation] = relations or []


class Relation(ASTNode):
    _children: ClassVar[tuple[str, str]] = ('leftExpression', 'rightExpression')

    def __init__(self, leftExpression: Expression|None = None, 
                 rightExpression: Expression|None = None, 
                 relationalOperator: TokenLexeme|None = None) -> None:
        
        self.leftExpression: Expression = leftExpression or Expression()
        self.rightExpression: Expression = rightExpression or Expression()
        self.relationalOperator: TokenLexeme = relationalOperator or TokenLexeme('T_NONE', '')

    def __repr__(self) -> str:
        tmp: str = ''
        tmp += str(self.leftExpression) + ' ' + self.relationalOperator.lexeme + ' ' + str(self.rightExpression)
        return tmp


class Expression(ASTNode):
    _children: ClassVar[tuple[str]] = ('terms',)

    def __init__(self, terms: list[TermTuple]|None = None) -> None:
        self.terms: list[TermTuple] = terms or []

        for term in self.terms[0:1]:
            if term.addOp.tokenType != 'T_NONE':
                raise ValueError('First term must not have an addOp')
        for term in self.terms[1:]:
            if term.addOp.tokenType != 'T_ADDOP':
                raise ValueError('All joining terms must have an addOp.')       

    def __repr__(self) -> str:
        tmp: str = ''  
      
        tmp += str(self.terms[0].term)
        for term in self.terms[1:]:
            tmp += ' ' + term.addOp.lexeme + ' ' + str(term.term)
        return tmp
    
    def addTerm(self, term: TermTuple) -> None:
        self.terms.append(term)

    def addTerms(self, terms: list[TermTuple]) -> None:
        for term in terms:
            self.addTerm(term)
        

class Term(ASTNode):
    _children: ClassVar[tuple[str]] = ('factors',)

    def __init__(self, factors: list[FactorTuple]|None = None) -> None:
        self.factors:list[FactorTuple] = factors or []

    def __repr__(self) -> str:
        tmp:str = ''
        tmp += str(self.factors[0].factor)
        for factor in self.factors[1:]:
            tmp += ' ' + factor.mulOp.lexeme + ' ' + str(factor.factor)
        return tmp

    def addFactor(self, factor: FactorTuple) -> None:
        self.factors.append(factor)
            

class Factor(ASTNode):
    _children: ClassVar[tuple[str, ...]] = ()

    def __init__(self, number: TokenLexeme|None = None, mulOp: TokenLexeme|None = None) -> None:
        self.number: TokenLexeme = number or TokenLexeme('T_NONE', ' ')
        self.mulOp: TokenLexeme = mulOp or TokenLexeme('T_NONE', '')

    def __repr__(self) -> str:
        tmp: str = ''
        if self.mulOp.tokenType != 'T_NONE':
            tmp += self.mulOp.lexeme + ' '
        tmp += self.number.lexeme
        return self.number.lexeme