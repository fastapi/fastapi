# Copyright 2004-2005 Elemental Security, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""This module defines the data structures used to represent a grammar.

These are a bit arcane because they are derived from the data
structures used by Python's 'pgen' parser generator.

There's also a table here mapping operators to their names in the
token module; the Python tokenize module reports all operators as the
fallback token code OP, but the parser needs the actual token code.

"""

# Python imports
import os
import pickle
import tempfile
from typing import Any, Dict, List, Optional, Text, Tuple, TypeVar, Union

# Local imports
from . import token

_P = TypeVar("_P", bound="Grammar")
Label = Tuple[int, Optional[Text]]
DFA = List[List[Tuple[int, int]]]
DFAS = Tuple[DFA, Dict[int, int]]
Path = Union[str, "os.PathLike[str]"]


class Grammar(object):
    """Pgen parsing tables conversion class.

    Once initialized, this class supplies the grammar tables for the
    parsing engine implemented by parse.py.  The parsing engine
    accesses the instance variables directly.  The class here does not
    provide initialization of the tables; several subclasses exist to
    do this (see the conv and pgen modules).

    The load() method reads the tables from a pickle file, which is
    much faster than the other ways offered by subclasses.  The pickle
    file is written by calling dump() (after loading the grammar
    tables using a subclass).  The report() method prints a readable
    representation of the tables to stdout, for debugging.

    The instance variables are as follows:

    symbol2number -- a dict mapping symbol names to numbers.  Symbol
                     numbers are always 256 or higher, to distinguish
                     them from token numbers, which are between 0 and
                     255 (inclusive).

    number2symbol -- a dict mapping numbers to symbol names;
                     these two are each other's inverse.

    states        -- a list of DFAs, where each DFA is a list of
                     states, each state is a list of arcs, and each
                     arc is a (i, j) pair where i is a label and j is
                     a state number.  The DFA number is the index into
                     this list.  (This name is slightly confusing.)
                     Final states are represented by a special arc of
                     the form (0, j) where j is its own state number.

    dfas          -- a dict mapping symbol numbers to (DFA, first)
                     pairs, where DFA is an item from the states list
                     above, and first is a set of tokens that can
                     begin this grammar rule (represented by a dict
                     whose values are always 1).

    labels        -- a list of (x, y) pairs where x is either a token
                     number or a symbol number, and y is either None
                     or a string; the strings are keywords.  The label
                     number is the index in this list; label numbers
                     are used to mark state transitions (arcs) in the
                     DFAs.

    start         -- the number of the grammar's start symbol.

    keywords      -- a dict mapping keyword strings to arc labels.

    tokens        -- a dict mapping token numbers to arc labels.

    """

    def __init__(self) -> None:
        self.symbol2number: Dict[str, int] = {}
        self.number2symbol: Dict[int, str] = {}
        self.states: List[DFA] = []
        self.dfas: Dict[int, DFAS] = {}
        self.labels: List[Label] = [(0, "EMPTY")]
        self.keywords: Dict[str, int] = {}
        self.soft_keywords: Dict[str, int] = {}
        self.tokens: Dict[int, int] = {}
        self.symbol2label: Dict[str, int] = {}
        self.version: Tuple[int, int] = (0, 0)
        self.start = 256
        # Python 3.7+ parses async as a keyword, not an identifier
        self.async_keywords = False

    def dump(self, filename: Path) -> None:
        """Dump the grammar tables to a pickle file."""

        # mypyc generates objects that don't have a __dict__, but they
        # do have __getstate__ methods that will return an equivalent
        # dictionary
        if hasattr(self, "__dict__"):
            d = self.__dict__
        else:
            d = self.__getstate__()  # type: ignore

        with tempfile.NamedTemporaryFile(
            dir=os.path.dirname(filename), delete=False
        ) as f:
            pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)
        os.replace(f.name, filename)

    def _update(self, attrs: Dict[str, Any]) -> None:
        for k, v in attrs.items():
            setattr(self, k, v)

    def load(self, filename: Path) -> None:
        """Load the grammar tables from a pickle file."""
        with open(filename, "rb") as f:
            d = pickle.load(f)
        self._update(d)

    def loads(self, pkl: bytes) -> None:
        """Load the grammar tables from a pickle bytes object."""
        self._update(pickle.loads(pkl))

    def copy(self: _P) -> _P:
        """
        Copy the grammar.
        """
        new = self.__class__()
        for dict_attr in (
            "symbol2number",
            "number2symbol",
            "dfas",
            "keywords",
            "soft_keywords",
            "tokens",
            "symbol2label",
        ):
            setattr(new, dict_attr, getattr(self, dict_attr).copy())
        new.labels = self.labels[:]
        new.states = self.states[:]
        new.start = self.start
        new.version = self.version
        new.async_keywords = self.async_keywords
        return new

    def report(self) -> None:
        """Dump the grammar tables to standard output, for debugging."""
        from pprint import pprint

        print("s2n")
        pprint(self.symbol2number)
        print("n2s")
        pprint(self.number2symbol)
        print("states")
        pprint(self.states)
        print("dfas")
        pprint(self.dfas)
        print("labels")
        pprint(self.labels)
        print("start", self.start)


# Map from operator to number (since tokenize doesn't do this)

opmap_raw = """
( LPAR
) RPAR
[ LSQB
] RSQB
: COLON
, COMMA
; SEMI
+ PLUS
- MINUS
* STAR
/ SLASH
| VBAR
& AMPER
< LESS
> GREATER
= EQUAL
. DOT
% PERCENT
` BACKQUOTE
{ LBRACE
} RBRACE
@ AT
@= ATEQUAL
== EQEQUAL
!= NOTEQUAL
<> NOTEQUAL
<= LESSEQUAL
>= GREATEREQUAL
~ TILDE
^ CIRCUMFLEX
<< LEFTSHIFT
>> RIGHTSHIFT
** DOUBLESTAR
+= PLUSEQUAL
-= MINEQUAL
*= STAREQUAL
/= SLASHEQUAL
%= PERCENTEQUAL
&= AMPEREQUAL
|= VBAREQUAL
^= CIRCUMFLEXEQUAL
<<= LEFTSHIFTEQUAL
>>= RIGHTSHIFTEQUAL
**= DOUBLESTAREQUAL
// DOUBLESLASH
//= DOUBLESLASHEQUAL
-> RARROW
:= COLONEQUAL
"""

opmap = {}
for line in opmap_raw.splitlines():
    if line:
        op, name = line.split()
        opmap[op] = getattr(token, name)
