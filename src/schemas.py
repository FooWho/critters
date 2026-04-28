from __future__ import annotations
from typing import NamedTuple
from parser import Condition, Command, Update, Action, Term, Expression

class Token(NamedTuple):
    tokenType: str|None
    lexeme: str
    line: int
    column: int

class TokenLexeme(NamedTuple):
    tokenType: str|None
    lexeme: str

class ConditionCommandTuple(NamedTuple):
    condition: Condition
    command: Command

class CommandTuple(NamedTuple):
    update: list[Update]
    action: Action

class RelationTuple(NamedTuple):
    leftExpression: Expression
    rightExpression: Expression
    relationalOperator: TokenLexeme

class TermTuple(NamedTuple):
    term: Term
    addOp: TokenLexeme

class CritterParseError(Exception):
    pass