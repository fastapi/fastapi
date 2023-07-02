"""Generic node traverser visitor"""

from __future__ import annotations

from mypy.nodes import Block, MypyFile
from mypy.traverser import TraverserVisitor


class TreeFreer(TraverserVisitor):
    def visit_block(self, block: Block) -> None:
        super().visit_block(block)
        block.body.clear()


def free_tree(tree: MypyFile) -> None:
    """Free all the ASTs associated with a module.

    This needs to be done recursively, since symbol tables contain
    references to definitions, so those won't be freed but we want their
    contents to be.
    """
    tree.accept(TreeFreer())
    tree.defs.clear()
