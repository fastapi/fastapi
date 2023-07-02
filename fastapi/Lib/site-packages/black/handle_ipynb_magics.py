"""Functions to process IPython magics with."""

import ast
import collections
import dataclasses
import secrets
import sys
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

if sys.version_info >= (3, 10):
    from typing import TypeGuard
else:
    from typing_extensions import TypeGuard

from black.output import out
from black.report import NothingChanged

TRANSFORMED_MAGICS = frozenset(
    (
        "get_ipython().run_cell_magic",
        "get_ipython().system",
        "get_ipython().getoutput",
        "get_ipython().run_line_magic",
    )
)
TOKENS_TO_IGNORE = frozenset(
    (
        "ENDMARKER",
        "NL",
        "NEWLINE",
        "COMMENT",
        "DEDENT",
        "UNIMPORTANT_WS",
        "ESCAPED_NL",
    )
)
PYTHON_CELL_MAGICS = frozenset(
    (
        "capture",
        "prun",
        "pypy",
        "python",
        "python3",
        "time",
        "timeit",
    )
)
TOKEN_HEX = secrets.token_hex


@dataclasses.dataclass(frozen=True)
class Replacement:
    mask: str
    src: str


@lru_cache()
def jupyter_dependencies_are_installed(*, verbose: bool, quiet: bool) -> bool:
    try:
        import IPython  # noqa:F401
        import tokenize_rt  # noqa:F401
    except ModuleNotFoundError:
        if verbose or not quiet:
            msg = (
                "Skipping .ipynb files as Jupyter dependencies are not installed.\n"
                'You can fix this by running ``pip install "black[jupyter]"``'
            )
            out(msg)
        return False
    else:
        return True


def remove_trailing_semicolon(src: str) -> Tuple[str, bool]:
    """Remove trailing semicolon from Jupyter notebook cell.

    For example,

        fig, ax = plt.subplots()
        ax.plot(x_data, y_data);  # plot data

    would become

        fig, ax = plt.subplots()
        ax.plot(x_data, y_data)  # plot data

    Mirrors the logic in `quiet` from `IPython.core.displayhook`, but uses
    ``tokenize_rt`` so that round-tripping works fine.
    """
    from tokenize_rt import reversed_enumerate, src_to_tokens, tokens_to_src

    tokens = src_to_tokens(src)
    trailing_semicolon = False
    for idx, token in reversed_enumerate(tokens):
        if token.name in TOKENS_TO_IGNORE:
            continue
        if token.name == "OP" and token.src == ";":
            del tokens[idx]
            trailing_semicolon = True
        break
    if not trailing_semicolon:
        return src, False
    return tokens_to_src(tokens), True


def put_trailing_semicolon_back(src: str, has_trailing_semicolon: bool) -> str:
    """Put trailing semicolon back if cell originally had it.

    Mirrors the logic in `quiet` from `IPython.core.displayhook`, but uses
    ``tokenize_rt`` so that round-tripping works fine.
    """
    if not has_trailing_semicolon:
        return src
    from tokenize_rt import reversed_enumerate, src_to_tokens, tokens_to_src

    tokens = src_to_tokens(src)
    for idx, token in reversed_enumerate(tokens):
        if token.name in TOKENS_TO_IGNORE:
            continue
        tokens[idx] = token._replace(src=token.src + ";")
        break
    else:  # pragma: nocover
        raise AssertionError(
            "INTERNAL ERROR: Was not able to reinstate trailing semicolon. "
            "Please report a bug on https://github.com/psf/black/issues.  "
        ) from None
    return str(tokens_to_src(tokens))


def mask_cell(src: str) -> Tuple[str, List[Replacement]]:
    """Mask IPython magics so content becomes parseable Python code.

    For example,

        %matplotlib inline
        'foo'

    becomes

        "25716f358c32750e"
        'foo'

    The replacements are returned, along with the transformed code.
    """
    replacements: List[Replacement] = []
    try:
        ast.parse(src)
    except SyntaxError:
        # Might have IPython magics, will process below.
        pass
    else:
        # Syntax is fine, nothing to mask, early return.
        return src, replacements

    from IPython.core.inputtransformer2 import TransformerManager

    transformer_manager = TransformerManager()
    transformed = transformer_manager.transform_cell(src)
    transformed, cell_magic_replacements = replace_cell_magics(transformed)
    replacements += cell_magic_replacements
    transformed = transformer_manager.transform_cell(transformed)
    transformed, magic_replacements = replace_magics(transformed)
    if len(transformed.splitlines()) != len(src.splitlines()):
        # Multi-line magic, not supported.
        raise NothingChanged
    replacements += magic_replacements
    return transformed, replacements


def get_token(src: str, magic: str) -> str:
    """Return randomly generated token to mask IPython magic with.

    For example, if 'magic' was `%matplotlib inline`, then a possible
    token to mask it with would be `"43fdd17f7e5ddc83"`. The token
    will be the same length as the magic, and we make sure that it was
    not already present anywhere else in the cell.
    """
    assert magic
    nbytes = max(len(magic) // 2 - 1, 1)
    token = TOKEN_HEX(nbytes)
    counter = 0
    while token in src:
        token = TOKEN_HEX(nbytes)
        counter += 1
        if counter > 100:
            raise AssertionError(
                "INTERNAL ERROR: Black was not able to replace IPython magic. "
                "Please report a bug on https://github.com/psf/black/issues.  "
                f"The magic might be helpful: {magic}"
            ) from None
    if len(token) + 2 < len(magic):
        token = f"{token}."
    return f'"{token}"'


def replace_cell_magics(src: str) -> Tuple[str, List[Replacement]]:
    """Replace cell magic with token.

    Note that 'src' will already have been processed by IPython's
    TransformerManager().transform_cell.

    Example,

        get_ipython().run_cell_magic('t', '-n1', 'ls =!ls\\n')

    becomes

        "a794."
        ls =!ls

    The replacement, along with the transformed code, is returned.
    """
    replacements: List[Replacement] = []

    tree = ast.parse(src)

    cell_magic_finder = CellMagicFinder()
    cell_magic_finder.visit(tree)
    if cell_magic_finder.cell_magic is None:
        return src, replacements
    header = cell_magic_finder.cell_magic.header
    mask = get_token(src, header)
    replacements.append(Replacement(mask=mask, src=header))
    return f"{mask}\n{cell_magic_finder.cell_magic.body}", replacements


def replace_magics(src: str) -> Tuple[str, List[Replacement]]:
    """Replace magics within body of cell.

    Note that 'src' will already have been processed by IPython's
    TransformerManager().transform_cell.

    Example, this

        get_ipython().run_line_magic('matplotlib', 'inline')
        'foo'

    becomes

        "5e67db56d490fd39"
        'foo'

    The replacement, along with the transformed code, are returned.
    """
    replacements = []
    magic_finder = MagicFinder()
    magic_finder.visit(ast.parse(src))
    new_srcs = []
    for i, line in enumerate(src.splitlines(), start=1):
        if i in magic_finder.magics:
            offsets_and_magics = magic_finder.magics[i]
            if len(offsets_and_magics) != 1:  # pragma: nocover
                raise AssertionError(
                    f"Expecting one magic per line, got: {offsets_and_magics}\n"
                    "Please report a bug on https://github.com/psf/black/issues."
                )
            col_offset, magic = (
                offsets_and_magics[0].col_offset,
                offsets_and_magics[0].magic,
            )
            mask = get_token(src, magic)
            replacements.append(Replacement(mask=mask, src=magic))
            line = line[:col_offset] + mask
        new_srcs.append(line)
    return "\n".join(new_srcs), replacements


def unmask_cell(src: str, replacements: List[Replacement]) -> str:
    """Remove replacements from cell.

    For example

        "9b20"
        foo = bar

    becomes

        %%time
        foo = bar
    """
    for replacement in replacements:
        src = src.replace(replacement.mask, replacement.src)
    return src


def _is_ipython_magic(node: ast.expr) -> TypeGuard[ast.Attribute]:
    """Check if attribute is IPython magic.

    Note that the source of the abstract syntax tree
    will already have been processed by IPython's
    TransformerManager().transform_cell.
    """
    return (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "get_ipython"
    )


def _get_str_args(args: List[ast.expr]) -> List[str]:
    str_args = []
    for arg in args:
        assert isinstance(arg, ast.Str)
        str_args.append(arg.s)
    return str_args


@dataclasses.dataclass(frozen=True)
class CellMagic:
    name: str
    params: Optional[str]
    body: str

    @property
    def header(self) -> str:
        if self.params:
            return f"%%{self.name} {self.params}"
        return f"%%{self.name}"


# ast.NodeVisitor + dataclass = breakage under mypyc.
class CellMagicFinder(ast.NodeVisitor):
    """Find cell magics.

    Note that the source of the abstract syntax tree
    will already have been processed by IPython's
    TransformerManager().transform_cell.

    For example,

        %%time\nfoo()

    would have been transformed to

        get_ipython().run_cell_magic('time', '', 'foo()\\n')

    and we look for instances of the latter.
    """

    def __init__(self, cell_magic: Optional[CellMagic] = None) -> None:
        self.cell_magic = cell_magic

    def visit_Expr(self, node: ast.Expr) -> None:
        """Find cell magic, extract header and body."""
        if (
            isinstance(node.value, ast.Call)
            and _is_ipython_magic(node.value.func)
            and node.value.func.attr == "run_cell_magic"
        ):
            args = _get_str_args(node.value.args)
            self.cell_magic = CellMagic(name=args[0], params=args[1], body=args[2])
        self.generic_visit(node)


@dataclasses.dataclass(frozen=True)
class OffsetAndMagic:
    col_offset: int
    magic: str


# Unsurprisingly, subclassing ast.NodeVisitor means we can't use dataclasses here
# as mypyc will generate broken code.
class MagicFinder(ast.NodeVisitor):
    """Visit cell to look for get_ipython calls.

    Note that the source of the abstract syntax tree
    will already have been processed by IPython's
    TransformerManager().transform_cell.

    For example,

        %matplotlib inline

    would have been transformed to

        get_ipython().run_line_magic('matplotlib', 'inline')

    and we look for instances of the latter (and likewise for other
    types of magics).
    """

    def __init__(self) -> None:
        self.magics: Dict[int, List[OffsetAndMagic]] = collections.defaultdict(list)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Look for system assign magics.

        For example,

            black_version = !black --version
            env = %env var

        would have been (respectively) transformed to

            black_version = get_ipython().getoutput('black --version')
            env = get_ipython().run_line_magic('env', 'var')

        and we look for instances of any of the latter.
        """
        if isinstance(node.value, ast.Call) and _is_ipython_magic(node.value.func):
            args = _get_str_args(node.value.args)
            if node.value.func.attr == "getoutput":
                src = f"!{args[0]}"
            elif node.value.func.attr == "run_line_magic":
                src = f"%{args[0]}"
                if args[1]:
                    src += f" {args[1]}"
            else:
                raise AssertionError(
                    f"Unexpected IPython magic {node.value.func.attr!r} found. "
                    "Please report a bug on https://github.com/psf/black/issues."
                ) from None
            self.magics[node.value.lineno].append(
                OffsetAndMagic(node.value.col_offset, src)
            )
        self.generic_visit(node)

    def visit_Expr(self, node: ast.Expr) -> None:
        """Look for magics in body of cell.

        For examples,

            !ls
            !!ls
            ?ls
            ??ls

        would (respectively) get transformed to

            get_ipython().system('ls')
            get_ipython().getoutput('ls')
            get_ipython().run_line_magic('pinfo', 'ls')
            get_ipython().run_line_magic('pinfo2', 'ls')

        and we look for instances of any of the latter.
        """
        if isinstance(node.value, ast.Call) and _is_ipython_magic(node.value.func):
            args = _get_str_args(node.value.args)
            if node.value.func.attr == "run_line_magic":
                if args[0] == "pinfo":
                    src = f"?{args[1]}"
                elif args[0] == "pinfo2":
                    src = f"??{args[1]}"
                else:
                    src = f"%{args[0]}"
                    if args[1]:
                        src += f" {args[1]}"
            elif node.value.func.attr == "system":
                src = f"!{args[0]}"
            elif node.value.func.attr == "getoutput":
                src = f"!!{args[0]}"
            else:
                raise NothingChanged  # unsupported magic.
            self.magics[node.value.lineno].append(
                OffsetAndMagic(node.value.col_offset, src)
            )
        self.generic_visit(node)
