"""
Root tag drawer.

"""

from .helpers import node_format


def svg(surface, node):
    """Draw a svg ``node``."""
    if node.parent is not None:
        width, height, viewbox = node_format(surface, node)
        surface.set_context_size(width, height, viewbox, node)
