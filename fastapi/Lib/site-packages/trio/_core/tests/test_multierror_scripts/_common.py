# https://coverage.readthedocs.io/en/latest/subprocess.html
try:
    import coverage
except ImportError:  # pragma: no cover
    pass
else:
    coverage.process_startup()
