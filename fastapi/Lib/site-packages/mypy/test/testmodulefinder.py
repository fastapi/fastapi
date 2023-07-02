from __future__ import annotations

import os

from mypy.modulefinder import FindModuleCache, ModuleNotFoundReason, SearchPaths
from mypy.options import Options
from mypy.test.config import package_path
from mypy.test.helpers import Suite, assert_equal

data_path = os.path.relpath(os.path.join(package_path, "modulefinder"))


class ModuleFinderSuite(Suite):
    def setUp(self) -> None:
        self.search_paths = SearchPaths(
            python_path=(),
            mypy_path=(
                os.path.join(data_path, "nsx-pkg1"),
                os.path.join(data_path, "nsx-pkg2"),
                os.path.join(data_path, "nsx-pkg3"),
                os.path.join(data_path, "nsy-pkg1"),
                os.path.join(data_path, "nsy-pkg2"),
                os.path.join(data_path, "pkg1"),
                os.path.join(data_path, "pkg2"),
            ),
            package_path=(),
            typeshed_path=(),
        )
        options = Options()
        options.namespace_packages = True
        self.fmc_ns = FindModuleCache(self.search_paths, fscache=None, options=options)

        options = Options()
        options.namespace_packages = False
        self.fmc_nons = FindModuleCache(
            self.search_paths, fscache=None, options=options
        )

    def test__no_namespace_packages__nsx(self) -> None:
        """
        If namespace_packages is False, we shouldn't find nsx
        """
        found_module = self.fmc_nons.find_module("nsx")
        assert_equal(ModuleNotFoundReason.NOT_FOUND, found_module)

    def test__no_namespace_packages__nsx_a(self) -> None:
        """
        If namespace_packages is False, we shouldn't find nsx.a.
        """
        found_module = self.fmc_nons.find_module("nsx.a")
        assert_equal(ModuleNotFoundReason.NOT_FOUND, found_module)

    def test__no_namespace_packages__find_a_in_pkg1(self) -> None:
        """
        Find find pkg1/a.py for "a" with namespace_packages False.
        """
        found_module = self.fmc_nons.find_module("a")
        expected = os.path.join(data_path, "pkg1", "a.py")
        assert_equal(expected, found_module)

    def test__no_namespace_packages__find_b_in_pkg2(self) -> None:
        found_module = self.fmc_ns.find_module("b")
        expected = os.path.join(data_path, "pkg2", "b", "__init__.py")
        assert_equal(expected, found_module)

    def test__find_nsx_as_namespace_pkg_in_pkg1(self) -> None:
        """
        There's no __init__.py in any of the nsx dirs, return
        the path to the first one found in mypypath.
        """
        found_module = self.fmc_ns.find_module("nsx")
        expected = os.path.join(data_path, "nsx-pkg1", "nsx")
        assert_equal(expected, found_module)

    def test__find_nsx_a_init_in_pkg1(self) -> None:
        """
        Find nsx-pkg1/nsx/a/__init__.py for "nsx.a" in namespace mode.
        """
        found_module = self.fmc_ns.find_module("nsx.a")
        expected = os.path.join(data_path, "nsx-pkg1", "nsx", "a", "__init__.py")
        assert_equal(expected, found_module)

    def test__find_nsx_b_init_in_pkg2(self) -> None:
        """
        Find nsx-pkg2/nsx/b/__init__.py for "nsx.b" in namespace mode.
        """
        found_module = self.fmc_ns.find_module("nsx.b")
        expected = os.path.join(data_path, "nsx-pkg2", "nsx", "b", "__init__.py")
        assert_equal(expected, found_module)

    def test__find_nsx_c_c_in_pkg3(self) -> None:
        """
        Find nsx-pkg3/nsx/c/c.py for "nsx.c.c" in namespace mode.
        """
        found_module = self.fmc_ns.find_module("nsx.c.c")
        expected = os.path.join(data_path, "nsx-pkg3", "nsx", "c", "c.py")
        assert_equal(expected, found_module)

    def test__find_nsy_a__init_pyi(self) -> None:
        """
        Prefer nsy-pkg1/a/__init__.pyi file over __init__.py.
        """
        found_module = self.fmc_ns.find_module("nsy.a")
        expected = os.path.join(data_path, "nsy-pkg1", "nsy", "a", "__init__.pyi")
        assert_equal(expected, found_module)

    def test__find_nsy_b__init_py(self) -> None:
        """
        There is a nsy-pkg2/nsy/b.pyi, but also a nsy-pkg2/nsy/b/__init__.py.
        We expect to find the latter when looking up "nsy.b" as
        a package is preferred over a module.
        """
        found_module = self.fmc_ns.find_module("nsy.b")
        expected = os.path.join(data_path, "nsy-pkg2", "nsy", "b", "__init__.py")
        assert_equal(expected, found_module)

    def test__find_nsy_c_pyi(self) -> None:
        """
        There is a nsy-pkg2/nsy/c.pyi and nsy-pkg2/nsy/c.py
        We expect to find the former when looking up "nsy.b" as
        .pyi is preferred over .py.
        """
        found_module = self.fmc_ns.find_module("nsy.c")
        expected = os.path.join(data_path, "nsy-pkg2", "nsy", "c.pyi")
        assert_equal(expected, found_module)

    def test__find_a_in_pkg1(self) -> None:
        found_module = self.fmc_ns.find_module("a")
        expected = os.path.join(data_path, "pkg1", "a.py")
        assert_equal(expected, found_module)

    def test__find_b_init_in_pkg2(self) -> None:
        found_module = self.fmc_ns.find_module("b")
        expected = os.path.join(data_path, "pkg2", "b", "__init__.py")
        assert_equal(expected, found_module)

    def test__find_d_nowhere(self) -> None:
        found_module = self.fmc_ns.find_module("d")
        assert_equal(ModuleNotFoundReason.NOT_FOUND, found_module)


class ModuleFinderSitePackagesSuite(Suite):
    def setUp(self) -> None:
        self.package_dir = os.path.relpath(
            os.path.join(package_path, "modulefinder-site-packages")
        )

        package_paths = (
            os.path.join(self.package_dir, "baz"),
            os.path.join(self.package_dir, "..", "not-a-directory"),
            os.path.join(self.package_dir, "..", "modulefinder-src"),
            self.package_dir,
        )

        self.search_paths = SearchPaths(
            python_path=(),
            mypy_path=(os.path.join(data_path, "pkg1"),),
            package_path=tuple(package_paths),
            typeshed_path=(),
        )
        options = Options()
        options.namespace_packages = True
        self.fmc_ns = FindModuleCache(self.search_paths, fscache=None, options=options)

        options = Options()
        options.namespace_packages = False
        self.fmc_nons = FindModuleCache(
            self.search_paths, fscache=None, options=options
        )

    def path(self, *parts: str) -> str:
        return os.path.join(self.package_dir, *parts)

    def test__packages_with_ns(self) -> None:
        cases = [
            # Namespace package with py.typed
            ("ns_pkg_typed", self.path("ns_pkg_typed")),
            ("ns_pkg_typed.a", self.path("ns_pkg_typed", "a.py")),
            ("ns_pkg_typed.b", self.path("ns_pkg_typed", "b")),
            ("ns_pkg_typed.b.c", self.path("ns_pkg_typed", "b", "c.py")),
            ("ns_pkg_typed.a.a_var", ModuleNotFoundReason.NOT_FOUND),
            # Namespace package without py.typed
            ("ns_pkg_untyped", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("ns_pkg_untyped.a", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("ns_pkg_untyped.b", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("ns_pkg_untyped.b.c", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("ns_pkg_untyped.a.a_var", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            # Namespace package without stub package
            ("ns_pkg_w_stubs", self.path("ns_pkg_w_stubs")),
            (
                "ns_pkg_w_stubs.typed",
                self.path("ns_pkg_w_stubs-stubs", "typed", "__init__.pyi"),
            ),
            (
                "ns_pkg_w_stubs.typed_inline",
                self.path("ns_pkg_w_stubs", "typed_inline", "__init__.py"),
            ),
            ("ns_pkg_w_stubs.untyped", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            # Regular package with py.typed
            ("pkg_typed", self.path("pkg_typed", "__init__.py")),
            ("pkg_typed.a", self.path("pkg_typed", "a.py")),
            ("pkg_typed.b", self.path("pkg_typed", "b", "__init__.py")),
            ("pkg_typed.b.c", self.path("pkg_typed", "b", "c.py")),
            ("pkg_typed.a.a_var", ModuleNotFoundReason.NOT_FOUND),
            # Regular package without py.typed
            ("pkg_untyped", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("pkg_untyped.a", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("pkg_untyped.b", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("pkg_untyped.b.c", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("pkg_untyped.a.a_var", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            # Top-level Python file in site-packages
            ("standalone", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            (
                "standalone.standalone_var",
                ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS,
            ),
            # Packages found by following .pth files
            ("baz_pkg", self.path("baz", "baz_pkg", "__init__.py")),
            ("ns_baz_pkg.a", self.path("baz", "ns_baz_pkg", "a.py")),
            (
                "neighbor_pkg",
                self.path("..", "modulefinder-src", "neighbor_pkg", "__init__.py"),
            ),
            (
                "ns_neighbor_pkg.a",
                self.path("..", "modulefinder-src", "ns_neighbor_pkg", "a.py"),
            ),
            # Something that doesn't exist
            ("does_not_exist", ModuleNotFoundReason.NOT_FOUND),
            # A regular package with an installed set of stubs
            ("foo.bar", self.path("foo-stubs", "bar.pyi")),
            # A regular, non-site-packages module
            ("a", os.path.join(data_path, "pkg1", "a.py")),
        ]
        for module, expected in cases:
            template = "Find(" + module + ") got {}; expected {}"

            actual = self.fmc_ns.find_module(module)
            assert_equal(actual, expected, template)

    def test__packages_without_ns(self) -> None:
        cases = [
            # Namespace package with py.typed
            ("ns_pkg_typed", ModuleNotFoundReason.NOT_FOUND),
            ("ns_pkg_typed.a", ModuleNotFoundReason.NOT_FOUND),
            ("ns_pkg_typed.b", ModuleNotFoundReason.NOT_FOUND),
            ("ns_pkg_typed.b.c", ModuleNotFoundReason.NOT_FOUND),
            ("ns_pkg_typed.a.a_var", ModuleNotFoundReason.NOT_FOUND),
            # Namespace package without py.typed
            ("ns_pkg_untyped", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("ns_pkg_untyped.a", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("ns_pkg_untyped.b", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("ns_pkg_untyped.b.c", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("ns_pkg_untyped.a.a_var", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            # Namespace package without stub package
            ("ns_pkg_w_stubs", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("ns_pkg_w_stubs.typed", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            (
                "ns_pkg_w_stubs.typed_inline",
                self.path("ns_pkg_w_stubs", "typed_inline", "__init__.py"),
            ),
            ("ns_pkg_w_stubs.untyped", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            # Regular package with py.typed
            ("pkg_typed", self.path("pkg_typed", "__init__.py")),
            ("pkg_typed.a", self.path("pkg_typed", "a.py")),
            ("pkg_typed.b", self.path("pkg_typed", "b", "__init__.py")),
            ("pkg_typed.b.c", self.path("pkg_typed", "b", "c.py")),
            ("pkg_typed.a.a_var", ModuleNotFoundReason.NOT_FOUND),
            # Regular package without py.typed
            ("pkg_untyped", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("pkg_untyped.a", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("pkg_untyped.b", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("pkg_untyped.b.c", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            ("pkg_untyped.a.a_var", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            # Top-level Python file in site-packages
            ("standalone", ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS),
            (
                "standalone.standalone_var",
                ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS,
            ),
            # Packages found by following .pth files
            ("baz_pkg", self.path("baz", "baz_pkg", "__init__.py")),
            ("ns_baz_pkg.a", ModuleNotFoundReason.NOT_FOUND),
            (
                "neighbor_pkg",
                self.path("..", "modulefinder-src", "neighbor_pkg", "__init__.py"),
            ),
            ("ns_neighbor_pkg.a", ModuleNotFoundReason.NOT_FOUND),
            # Something that doesn't exist
            ("does_not_exist", ModuleNotFoundReason.NOT_FOUND),
            # A regular package with an installed set of stubs
            ("foo.bar", self.path("foo-stubs", "bar.pyi")),
            # A regular, non-site-packages module
            ("a", os.path.join(data_path, "pkg1", "a.py")),
        ]
        for module, expected in cases:
            template = "Find(" + module + ") got {}; expected {}"

            actual = self.fmc_nons.find_module(module)
            assert_equal(actual, expected, template)
