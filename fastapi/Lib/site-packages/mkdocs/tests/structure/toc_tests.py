#!/usr/bin/env python

import unittest

from mkdocs.structure.toc import get_toc
from mkdocs.tests.base import dedent, get_markdown_toc


class TableOfContentsTests(unittest.TestCase):
    def test_indented_toc(self):
        md = dedent(
            """
            # Heading 1
            ## Heading 2
            ### Heading 3
            """
        )
        expected = dedent(
            """
            Heading 1 - #heading-1
                Heading 2 - #heading-2
                    Heading 3 - #heading-3
            """
        )
        toc = get_toc(get_markdown_toc(md))
        self.assertEqual(str(toc).strip(), expected)
        self.assertEqual(len(toc), 1)

    def test_indented_toc_html(self):
        md = dedent(
            """
            # Heading 1
            ## <code>Heading</code> 2
            ## Heading 3
            """
        )
        expected = dedent(
            """
            Heading 1 - #heading-1
                Heading 2 - #heading-2
                Heading 3 - #heading-3
            """
        )
        toc = get_toc(get_markdown_toc(md))
        self.assertEqual(str(toc).strip(), expected)
        self.assertEqual(len(toc), 1)

    def test_flat_toc(self):
        md = dedent(
            """
            # Heading 1
            # Heading 2
            # Heading 3
            """
        )
        expected = dedent(
            """
            Heading 1 - #heading-1
            Heading 2 - #heading-2
            Heading 3 - #heading-3
            """
        )
        toc = get_toc(get_markdown_toc(md))
        self.assertEqual(str(toc).strip(), expected)
        self.assertEqual(len(toc), 3)

    def test_flat_h2_toc(self):
        md = dedent(
            """
            ## Heading 1
            ## Heading 2
            ## Heading 3
            """
        )
        expected = dedent(
            """
            Heading 1 - #heading-1
            Heading 2 - #heading-2
            Heading 3 - #heading-3
            """
        )
        toc = get_toc(get_markdown_toc(md))
        self.assertEqual(str(toc).strip(), expected)
        self.assertEqual(len(toc), 3)

    def test_mixed_toc(self):
        md = dedent(
            """
            # Heading 1
            ## Heading 2
            # Heading 3
            ### Heading 4
            ### Heading 5
            """
        )
        expected = dedent(
            """
            Heading 1 - #heading-1
                Heading 2 - #heading-2
            Heading 3 - #heading-3
                Heading 4 - #heading-4
                Heading 5 - #heading-5
            """
        )
        toc = get_toc(get_markdown_toc(md))
        self.assertEqual(str(toc).strip(), expected)
        self.assertEqual(len(toc), 2)

    def test_mixed_html(self):
        md = dedent(
            """
            # Heading 1
            ## Heading 2
            # Heading 3
            ### Heading 4
            ### <a>Heading 5</a>
            """
        )
        expected = dedent(
            """
            Heading 1 - #heading-1
                Heading 2 - #heading-2
            Heading 3 - #heading-3
                Heading 4 - #heading-4
                Heading 5 - #heading-5
            """
        )
        toc = get_toc(get_markdown_toc(md))
        self.assertEqual(str(toc).strip(), expected)
        self.assertEqual(len(toc), 2)

    def test_nested_anchor(self):
        md = dedent(
            """
            # Heading 1
            ## Heading 2
            # Heading 3
            ### Heading 4
            ### <a href="/">Heading 5</a>
            """
        )
        expected = dedent(
            """
            Heading 1 - #heading-1
                Heading 2 - #heading-2
            Heading 3 - #heading-3
                Heading 4 - #heading-4
                Heading 5 - #heading-5
            """
        )
        toc = get_toc(get_markdown_toc(md))
        self.assertEqual(str(toc).strip(), expected)
        self.assertEqual(len(toc), 2)

    def test_entityref(self):
        md = dedent(
            """
            # Heading & 1
            ## Heading > 2
            ### Heading < 3
            """
        )
        expected = dedent(
            """
            Heading &amp; 1 - #heading-1
                Heading &gt; 2 - #heading-2
                    Heading &lt; 3 - #heading-3
            """
        )
        toc = get_toc(get_markdown_toc(md))
        self.assertEqual(str(toc).strip(), expected)
        self.assertEqual(len(toc), 1)

    def test_charref(self):
        md = "# &#64;Header"
        expected = "&#64;Header - #header"
        toc = get_toc(get_markdown_toc(md))
        self.assertEqual(str(toc).strip(), expected)
        self.assertEqual(len(toc), 1)

    def test_level(self):
        md = dedent(
            """
            # Heading 1
            ## Heading 1.1
            ### Heading 1.1.1
            ### Heading 1.1.2
            ## Heading 1.2
            """
        )
        toc = get_toc(get_markdown_toc(md))

        def get_level_sequence(items):
            for item in items:
                yield item.level
                yield from get_level_sequence(item.children)

        self.assertEqual(tuple(get_level_sequence(toc)), (1, 2, 3, 3, 2))
