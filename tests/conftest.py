import sys

if sys.version_info < (3, 12):
    collect_ignore_glob = ["*_py312.py"]
