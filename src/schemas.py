from __future__ import annotations
from typing import NamedTuple

class Token(NamedTuple):
    tokenType: str|None
    lexeme: str
    line: int
    column: int

class TokenLexeme(NamedTuple):
    tokenType: str|None
    lexeme: str

class CritterParseError(Exception):
    pass