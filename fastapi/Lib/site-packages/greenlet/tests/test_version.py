#! /usr/bin/env python
from __future__ import absolute_import, print_function

import os
import sys
from unittest import TestCase as NonLeakingTestCase

import greenlet


# No reason to run this multiple times under leakchecks,
# it doesn't do anything.
class VersionTests(NonLeakingTestCase):
    def test_version(self):
        def find_dominating_file(name):
            if os.path.exists(name):
                return name

            tried = []
            here = os.path.abspath(os.path.dirname(__file__))
            for i in range(10):
                up = [".."] * i
                path = [here] + up + [name]
                fname = os.path.join(*path)
                fname = os.path.abspath(fname)
                tried.append(fname)
                if os.path.exists(fname):
                    return fname
            raise AssertionError(
                "Could not find file " + name + "; checked " + str(tried)
            )

        try:
            setup_py = find_dominating_file("setup.py")
        except AssertionError as e:
            self.skipTest("Unable to find setup.py; must be out of tree. " + str(e))

        invoke_setup = "%s %s --version" % (sys.executable, setup_py)
        with os.popen(invoke_setup) as f:
            sversion = f.read().strip()

        self.assertEqual(sversion, greenlet.__version__)
