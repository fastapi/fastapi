#!/usr/bin/env python

import os
import unittest

from mkdocs.commands import new
from mkdocs.tests.base import change_dir, tempdir


class NewTests(unittest.TestCase):
    @tempdir()
    def test_new(self, temp_dir):
        with change_dir(temp_dir):
            new.new("myproject")

            expected_paths = [
                os.path.join(temp_dir, "myproject"),
                os.path.join(temp_dir, "myproject", "mkdocs.yml"),
                os.path.join(temp_dir, "myproject", "docs"),
                os.path.join(temp_dir, "myproject", "docs", "index.md"),
            ]

            for expected_path in expected_paths:
                self.assertTrue(os.path.exists(expected_path))
