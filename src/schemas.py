from __future__ import annotations
from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from parser import Condition, Command, Update, Action, Term, Expression, Factor

class Token(NamedTuple):
    tokenType: str
    lexeme: str
    line: int
    column: int

class TokenLexeme(NamedTuple):
    tokenType: str
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
    addOp: TokenLexeme
    term: Term

class FactorTuple(NamedTuple):
    mulOp: TokenLexeme
    factor: Factor


class CritterParseError(Exception):
    pass