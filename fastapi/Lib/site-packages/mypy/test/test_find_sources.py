from __future__ import annotations

import os
import shutil
import tempfile
import unittest

import pytest

from mypy.find_sources import InvalidSourceList, SourceFinder, create_source_list
from mypy.fscache import FileSystemCache
from mypy.modulefinder import BuildSource
from mypy.options import Options


class FakeFSCache(FileSystemCache):
    def __init__(self, files: set[str]) -> None:
        self.files = {os.path.abspath(f) for f in files}

    def isfile(self, file: str) -> bool:
        return file in self.files

    def isdir(self, dir: str) -> bool:
        if not dir.endswith(os.sep):
            dir += os.sep
        return any(f.startswith(dir) for f in self.files)

    def listdir(self, dir: str) -> list[str]:
        if not dir.endswith(os.sep):
            dir += os.sep
        return list(
            {f[len(dir) :].split(os.sep)[0] for f in self.files if f.startswith(dir)}
        )

    def init_under_package_root(self, file: str) -> bool:
        return False


def normalise_path(path: str) -> str:
    path = os.path.splitdrive(path)[1]
    path = path.replace(os.sep, "/")
    return path


def normalise_build_source_list(
    sources: list[BuildSource],
) -> list[tuple[str, str | None]]:
    return sorted(
        (s.module, (normalise_path(s.base_dir) if s.base_dir is not None else None))
        for s in sources
    )


def crawl(finder: SourceFinder, f: str) -> tuple[str, str]:
    module, base_dir = finder.crawl_up(f)
    return module, normalise_path(base_dir)


def find_sources_in_dir(finder: SourceFinder, f: str) -> list[tuple[str, str | None]]:
    return normalise_build_source_list(finder.find_sources_in_dir(os.path.abspath(f)))


def find_sources(
    paths: list[str], options: Options, fscache: FileSystemCache
) -> list[tuple[str, str | None]]:
    paths = [os.path.abspath(p) for p in paths]
    return normalise_build_source_list(create_source_list(paths, options, fscache))


class SourceFinderSuite(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.mkdtemp()
        self.oldcwd = os.getcwd()
        os.chdir(self.tempdir)

    def tearDown(self) -> None:
        os.chdir(self.oldcwd)
        shutil.rmtree(self.tempdir)

    def test_crawl_no_namespace(self) -> None:
        options = Options()
        options.namespace_packages = False

        finder = SourceFinder(FakeFSCache({"/setup.py"}), options)
        assert crawl(finder, "/setup.py") == ("setup", "/")

        finder = SourceFinder(FakeFSCache({"/a/setup.py"}), options)
        assert crawl(finder, "/a/setup.py") == ("setup", "/a")

        finder = SourceFinder(FakeFSCache({"/a/b/setup.py"}), options)
        assert crawl(finder, "/a/b/setup.py") == ("setup", "/a/b")

        finder = SourceFinder(FakeFSCache({"/a/setup.py", "/a/__init__.py"}), options)
        assert crawl(finder, "/a/setup.py") == ("a.setup", "/")

        finder = SourceFinder(
            FakeFSCache({"/a/invalid-name/setup.py", "/a/__init__.py"}), options
        )
        assert crawl(finder, "/a/invalid-name/setup.py") == ("setup", "/a/invalid-name")

        finder = SourceFinder(FakeFSCache({"/a/b/setup.py", "/a/__init__.py"}), options)
        assert crawl(finder, "/a/b/setup.py") == ("setup", "/a/b")

        finder = SourceFinder(
            FakeFSCache({"/a/b/c/setup.py", "/a/__init__.py", "/a/b/c/__init__.py"}),
            options,
        )
        assert crawl(finder, "/a/b/c/setup.py") == ("c.setup", "/a/b")

    def test_crawl_namespace(self) -> None:
        options = Options()
        options.namespace_packages = True

        finder = SourceFinder(FakeFSCache({"/setup.py"}), options)
        assert crawl(finder, "/setup.py") == ("setup", "/")

        finder = SourceFinder(FakeFSCache({"/a/setup.py"}), options)
        assert crawl(finder, "/a/setup.py") == ("setup", "/a")

        finder = SourceFinder(FakeFSCache({"/a/b/setup.py"}), options)
        assert crawl(finder, "/a/b/setup.py") == ("setup", "/a/b")

        finder = SourceFinder(FakeFSCache({"/a/setup.py", "/a/__init__.py"}), options)
        assert crawl(finder, "/a/setup.py") == ("a.setup", "/")

        finder = SourceFinder(
            FakeFSCache({"/a/invalid-name/setup.py", "/a/__init__.py"}), options
        )
        assert crawl(finder, "/a/invalid-name/setup.py") == ("setup", "/a/invalid-name")

        finder = SourceFinder(FakeFSCache({"/a/b/setup.py", "/a/__init__.py"}), options)
        assert crawl(finder, "/a/b/setup.py") == ("a.b.setup", "/")

        finder = SourceFinder(
            FakeFSCache({"/a/b/c/setup.py", "/a/__init__.py", "/a/b/c/__init__.py"}),
            options,
        )
        assert crawl(finder, "/a/b/c/setup.py") == ("a.b.c.setup", "/")

    def test_crawl_namespace_explicit_base(self) -> None:
        options = Options()
        options.namespace_packages = True
        options.explicit_package_bases = True

        finder = SourceFinder(FakeFSCache({"/setup.py"}), options)
        assert crawl(finder, "/setup.py") == ("setup", "/")

        finder = SourceFinder(FakeFSCache({"/a/setup.py"}), options)
        assert crawl(finder, "/a/setup.py") == ("setup", "/a")

        finder = SourceFinder(FakeFSCache({"/a/b/setup.py"}), options)
        assert crawl(finder, "/a/b/setup.py") == ("setup", "/a/b")

        finder = SourceFinder(FakeFSCache({"/a/setup.py", "/a/__init__.py"}), options)
        assert crawl(finder, "/a/setup.py") == ("a.setup", "/")

        finder = SourceFinder(
            FakeFSCache({"/a/invalid-name/setup.py", "/a/__init__.py"}), options
        )
        assert crawl(finder, "/a/invalid-name/setup.py") == ("setup", "/a/invalid-name")

        finder = SourceFinder(FakeFSCache({"/a/b/setup.py", "/a/__init__.py"}), options)
        assert crawl(finder, "/a/b/setup.py") == ("a.b.setup", "/")

        finder = SourceFinder(
            FakeFSCache({"/a/b/c/setup.py", "/a/__init__.py", "/a/b/c/__init__.py"}),
            options,
        )
        assert crawl(finder, "/a/b/c/setup.py") == ("a.b.c.setup", "/")

        # set mypy path, so we actually have some explicit base dirs
        options.mypy_path = ["/a/b"]

        finder = SourceFinder(FakeFSCache({"/a/b/c/setup.py"}), options)
        assert crawl(finder, "/a/b/c/setup.py") == ("c.setup", "/a/b")

        finder = SourceFinder(
            FakeFSCache({"/a/b/c/setup.py", "/a/__init__.py", "/a/b/c/__init__.py"}),
            options,
        )
        assert crawl(finder, "/a/b/c/setup.py") == ("c.setup", "/a/b")

        options.mypy_path = ["/a/b", "/a/b/c"]
        finder = SourceFinder(FakeFSCache({"/a/b/c/setup.py"}), options)
        assert crawl(finder, "/a/b/c/setup.py") == ("setup", "/a/b/c")

    def test_crawl_namespace_multi_dir(self) -> None:
        options = Options()
        options.namespace_packages = True
        options.explicit_package_bases = True
        options.mypy_path = ["/a", "/b"]

        finder = SourceFinder(FakeFSCache({"/a/pkg/a.py", "/b/pkg/b.py"}), options)
        assert crawl(finder, "/a/pkg/a.py") == ("pkg.a", "/a")
        assert crawl(finder, "/b/pkg/b.py") == ("pkg.b", "/b")

    def test_find_sources_in_dir_no_namespace(self) -> None:
        options = Options()
        options.namespace_packages = False

        files = {
            "/pkg/a1/b/c/d/e.py",
            "/pkg/a1/b/f.py",
            "/pkg/a2/__init__.py",
            "/pkg/a2/b/c/d/e.py",
            "/pkg/a2/b/f.py",
        }
        finder = SourceFinder(FakeFSCache(files), options)
        assert find_sources_in_dir(finder, "/") == [
            ("a2", "/pkg"),
            ("e", "/pkg/a1/b/c/d"),
            ("e", "/pkg/a2/b/c/d"),
            ("f", "/pkg/a1/b"),
            ("f", "/pkg/a2/b"),
        ]

    def test_find_sources_in_dir_namespace(self) -> None:
        options = Options()
        options.namespace_packages = True

        files = {
            "/pkg/a1/b/c/d/e.py",
            "/pkg/a1/b/f.py",
            "/pkg/a2/__init__.py",
            "/pkg/a2/b/c/d/e.py",
            "/pkg/a2/b/f.py",
        }
        finder = SourceFinder(FakeFSCache(files), options)
        assert find_sources_in_dir(finder, "/") == [
            ("a2", "/pkg"),
            ("a2.b.c.d.e", "/pkg"),
            ("a2.b.f", "/pkg"),
            ("e", "/pkg/a1/b/c/d"),
            ("f", "/pkg/a1/b"),
        ]

    def test_find_sources_in_dir_namespace_explicit_base(self) -> None:
        options = Options()
        options.namespace_packages = True
        options.explicit_package_bases = True
        options.mypy_path = ["/"]

        files = {
            "/pkg/a1/b/c/d/e.py",
            "/pkg/a1/b/f.py",
            "/pkg/a2/__init__.py",
            "/pkg/a2/b/c/d/e.py",
            "/pkg/a2/b/f.py",
        }
        finder = SourceFinder(FakeFSCache(files), options)
        assert find_sources_in_dir(finder, "/") == [
            ("pkg.a1.b.c.d.e", "/"),
            ("pkg.a1.b.f", "/"),
            ("pkg.a2", "/"),
            ("pkg.a2.b.c.d.e", "/"),
            ("pkg.a2.b.f", "/"),
        ]

        options.mypy_path = ["/pkg"]
        finder = SourceFinder(FakeFSCache(files), options)
        assert find_sources_in_dir(finder, "/") == [
            ("a1.b.c.d.e", "/pkg"),
            ("a1.b.f", "/pkg"),
            ("a2", "/pkg"),
            ("a2.b.c.d.e", "/pkg"),
            ("a2.b.f", "/pkg"),
        ]

    def test_find_sources_in_dir_namespace_multi_dir(self) -> None:
        options = Options()
        options.namespace_packages = True
        options.explicit_package_bases = True
        options.mypy_path = ["/a", "/b"]

        finder = SourceFinder(FakeFSCache({"/a/pkg/a.py", "/b/pkg/b.py"}), options)
        assert find_sources_in_dir(finder, "/") == [("pkg.a", "/a"), ("pkg.b", "/b")]

    def test_find_sources_exclude(self) -> None:
        options = Options()
        options.namespace_packages = True

        # default
        for excluded_dir in ["site-packages", ".whatever", "node_modules", ".x/.z"]:
            fscache = FakeFSCache({"/dir/a.py", f"/dir/venv/{excluded_dir}/b.py"})
            assert find_sources(["/"], options, fscache) == [("a", "/dir")]
            with pytest.raises(InvalidSourceList):
                find_sources(["/dir/venv/"], options, fscache)
            assert find_sources([f"/dir/venv/{excluded_dir}"], options, fscache) == [
                ("b", f"/dir/venv/{excluded_dir}")
            ]
            assert find_sources(
                [f"/dir/venv/{excluded_dir}/b.py"], options, fscache
            ) == [("b", f"/dir/venv/{excluded_dir}")]

        files = {
            "/pkg/a1/b/c/d/e.py",
            "/pkg/a1/b/f.py",
            "/pkg/a2/__init__.py",
            "/pkg/a2/b/c/d/e.py",
            "/pkg/a2/b/f.py",
        }

        # file name
        options.exclude = [r"/f\.py$"]
        fscache = FakeFSCache(files)
        assert find_sources(["/"], options, fscache) == [
            ("a2", "/pkg"),
            ("a2.b.c.d.e", "/pkg"),
            ("e", "/pkg/a1/b/c/d"),
        ]
        assert find_sources(["/pkg/a1/b/f.py"], options, fscache) == [
            ("f", "/pkg/a1/b")
        ]
        assert find_sources(["/pkg/a2/b/f.py"], options, fscache) == [
            ("a2.b.f", "/pkg")
        ]

        # directory name
        options.exclude = ["/a1/"]
        fscache = FakeFSCache(files)
        assert find_sources(["/"], options, fscache) == [
            ("a2", "/pkg"),
            ("a2.b.c.d.e", "/pkg"),
            ("a2.b.f", "/pkg"),
        ]
        with pytest.raises(InvalidSourceList):
            find_sources(["/pkg/a1"], options, fscache)
        with pytest.raises(InvalidSourceList):
            find_sources(["/pkg/a1/"], options, fscache)
        with pytest.raises(InvalidSourceList):
            find_sources(["/pkg/a1/b"], options, fscache)

        options.exclude = ["/a1/$"]
        assert find_sources(["/pkg/a1"], options, fscache) == [
            ("e", "/pkg/a1/b/c/d"),
            ("f", "/pkg/a1/b"),
        ]

        # paths
        options.exclude = ["/pkg/a1/"]
        fscache = FakeFSCache(files)
        assert find_sources(["/"], options, fscache) == [
            ("a2", "/pkg"),
            ("a2.b.c.d.e", "/pkg"),
            ("a2.b.f", "/pkg"),
        ]
        with pytest.raises(InvalidSourceList):
            find_sources(["/pkg/a1"], options, fscache)

        # OR two patterns together
        for orred in [["/(a1|a3)/"], ["a1", "a3"], ["a3", "a1"]]:
            options.exclude = orred
            fscache = FakeFSCache(files)
            assert find_sources(["/"], options, fscache) == [
                ("a2", "/pkg"),
                ("a2.b.c.d.e", "/pkg"),
                ("a2.b.f", "/pkg"),
            ]

        options.exclude = ["b/c/"]
        fscache = FakeFSCache(files)
        assert find_sources(["/"], options, fscache) == [
            ("a2", "/pkg"),
            ("a2.b.f", "/pkg"),
            ("f", "/pkg/a1/b"),
        ]

        # nothing should be ignored as a result of this
        big_exclude1 = [
            "/pkg/a/",
            "/2",
            "/1",
            "/pk/",
            "/kg",
            "/g.py",
            "/bc",
            "/xxx/pkg/a2/b/f.py",
            "xxx/pkg/a2/b/f.py",
        ]
        big_exclude2 = ["|".join(big_exclude1)]
        for big_exclude in [big_exclude1, big_exclude2]:
            options.exclude = big_exclude
            fscache = FakeFSCache(files)
            assert len(find_sources(["/"], options, fscache)) == len(files)

            files = {
                "pkg/a1/b/c/d/e.py",
                "pkg/a1/b/f.py",
                "pkg/a2/__init__.py",
                "pkg/a2/b/c/d/e.py",
                "pkg/a2/b/f.py",
            }
            fscache = FakeFSCache(files)
            assert len(find_sources(["."], options, fscache)) == len(files)
