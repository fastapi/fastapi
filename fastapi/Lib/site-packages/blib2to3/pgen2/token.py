"""Token constants (from "token.h")."""

import sys
from typing import Dict

if sys.version_info < (3, 8):
    from typing_extensions import Final
else:
    from typing import Final

#  Taken from Python (r53757) and modified to include some tokens
#   originally monkeypatched in by pgen2.tokenize

# --start constants--
ENDMARKER: Final = 0
NAME: Final = 1
NUMBER: Final = 2
STRING: Final = 3
NEWLINE: Final = 4
INDENT: Final = 5
DEDENT: Final = 6
LPAR: Final = 7
RPAR: Final = 8
LSQB: Final = 9
RSQB: Final = 10
COLON: Final = 11
COMMA: Final = 12
SEMI: Final = 13
PLUS: Final = 14
MINUS: Final = 15
STAR: Final = 16
SLASH: Final = 17
VBAR: Final = 18
AMPER: Final = 19
LESS: Final = 20
GREATER: Final = 21
EQUAL: Final = 22
DOT: Final = 23
PERCENT: Final = 24
BACKQUOTE: Final = 25
LBRACE: Final = 26
RBRACE: Final = 27
EQEQUAL: Final = 28
NOTEQUAL: Final = 29
LESSEQUAL: Final = 30
GREATEREQUAL: Final = 31
TILDE: Final = 32
CIRCUMFLEX: Final = 33
LEFTSHIFT: Final = 34
RIGHTSHIFT: Final = 35
DOUBLESTAR: Final = 36
PLUSEQUAL: Final = 37
MINEQUAL: Final = 38
STAREQUAL: Final = 39
SLASHEQUAL: Final = 40
PERCENTEQUAL: Final = 41
AMPEREQUAL: Final = 42
VBAREQUAL: Final = 43
CIRCUMFLEXEQUAL: Final = 44
LEFTSHIFTEQUAL: Final = 45
RIGHTSHIFTEQUAL: Final = 46
DOUBLESTAREQUAL: Final = 47
DOUBLESLASH: Final = 48
DOUBLESLASHEQUAL: Final = 49
AT: Final = 50
ATEQUAL: Final = 51
OP: Final = 52
COMMENT: Final = 53
NL: Final = 54
RARROW: Final = 55
AWAIT: Final = 56
ASYNC: Final = 57
ERRORTOKEN: Final = 58
COLONEQUAL: Final = 59
N_TOKENS: Final = 60
NT_OFFSET: Final = 256
# --end constants--

tok_name: Final[Dict[int, str]] = {}
for _name, _value in list(globals().items()):
    if type(_value) is type(0):
        tok_name[_value] = _name


def ISTERMINAL(x: int) -> bool:
    return x < NT_OFFSET


def ISNONTERMINAL(x: int) -> bool:
    return x >= NT_OFFSET


def ISEOF(x: int) -> bool:
    return x == ENDMARKER
