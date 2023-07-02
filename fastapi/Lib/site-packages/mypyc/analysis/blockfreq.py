"""Find basic blocks that are likely to be executed frequently.

For example, this would not include blocks that have exception handlers.

We can use different optimization heuristics for common and rare code. For
example, we can make IR fast to compile instead of fast to execute for rare
code.
"""

from __future__ import annotations

from mypyc.ir.ops import BasicBlock, Branch, Goto


def frequently_executed_blocks(entry_point: BasicBlock) -> set[BasicBlock]:
    result: set[BasicBlock] = set()
    worklist = [entry_point]
    while worklist:
        block = worklist.pop()
        if block in result:
            continue
        result.add(block)
        t = block.terminator
        if isinstance(t, Goto):
            worklist.append(t.label)
        elif isinstance(t, Branch):
            if t.rare or t.traceback_entry is not None:
                worklist.append(t.false)
            else:
                worklist.append(t.true)
                worklist.append(t.false)
    return result
