import re
from enum import StrEnum

class Pattern(StrEnum):
    MULOP = r"\*|/|mod"

matches = re.finditer(Pattern.MULOP, "*")

