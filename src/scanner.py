import re
from enum import StrEnum

class Terminals(StrEnum):
    T_STAR = r"\*"
    T_DIV = r"/"
    T_MOD = r"mod"
    T_PLUS = r"\+"
    T_MINUS = r"\-"
    T_LESS = r"<"
    T_GREAT = r">"
    T_LEQU = r"<="
    T_GEQU = r">="
    T_NEQU = r"!="
    T_EQU = r"="
    T_ASSIGN = r":="
    T_L_PAREN = r"\("
    T_R_PAREN = r"\)"
    T_L_BRACKET = r"\["
    T_R_BRACKET = r"\]"
    T_L_BRACE = r"\{"
    T_R_BRACE = r"\}"
    T_NEARBY = r"nearby"
    T_AHEAD = r"ahead"
    T_RANDOM = r"random"
    T_SMELL = r"SMELL"
    T_AND = r"and"
    T_OR = r"or"
    T_WAIT = r"wait"
    T_FORWARD = r"forward"
    T_BACKWARD = r"backward"
    T_LEFT = r"left"
    T_RIGHT = r"right"
    T_EAT = r"eat"
    T_ATTACK = r"attack"
    T_GROW = r"grow"
    T_BUD = r"bud"
    T_SERVE = r"serve"
    T_COMM = r"-->"
    T_NUMBER = r"\d+"
    T_SEMICOLON = r";"


    
   

pattern = (
    f'{Terminals.T_PLUS}|{Terminals.T_MINUS}|{Terminals.T_LESS}|'
    f'{Terminals.T_GREAT}|{Terminals.T_LEQU}|{Terminals.T_GEQU}|'
    f'{Terminals.T_NEQU}|{Terminals.T_EQU}|{Terminals.T_ASSIGN}|'
    f'{Terminals.T_L_PAREN}|{Terminals.T_R_PAREN}|{Terminals.T_L_BRACKET}|'
    f'{Terminals.T_R_BRACKET}|{Terminals.T_L_BRACE}|{Terminals.T_R_BRACE}|'
    f'{Terminals.T_NEARBY}|{Terminals.T_AHEAD}|{Terminals.T_RANDOM}|'
    f'{Terminals.T_SMELL}|{Terminals.T_AND}|{Terminals.T_OR}|'
    f'{Terminals.T_WAIT}|{Terminals.T_FORWARD}|{Terminals.T_BACKWARD}|'
    f'{Terminals.T_LEFT}|{Terminals.T_RIGHT}|{Terminals.T_EAT}|'
    f'{Terminals.T_ATTACK}|{Terminals.T_GROW}|{Terminals.T_BUD}|'
    f'{Terminals.T_SERVE}|{Terminals.T_COMM}|{Terminals.T_NUMBER}|'
    f'{Terminals.T_SEMICOLON}'
)
line = "ahead[3] < -15 and ahead[1] = 0 --> forward;"
matches = re.finditer(pattern, line)
token = next(matches, None)
while token != None:
    print(f'Matched: {token.group()}')
    token = next(matches, None)
print("All matches found.")


