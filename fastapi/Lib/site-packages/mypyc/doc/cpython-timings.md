# Timings of CPython Operations

Here are some *very rough* approximate timings of CPython interpreter
operations:

* `f(1)` (empty function body): 70-90ns
* `f(n=1)` (empty function body): 90-110ns
* `o.x`: 30-40ns
* `o.f(1)` (empty method body): 80-160ns
* `Cls(1)` (initialize attribute in `__init__`): 290-330ns
* `x + y` (integers): 20-35ns
* `a[i]` (list) : 20-40ns
* `[i]` (also dealloc): 35-55ns
* `a.append(i)` (list, average over 5 appends): 70ns
* `d[s]` (dict, shared str key): 20ns
* `d[s] = i` (dict, shared str key): 40ns
* `isinstance(x, A)`: 100ns
* `(x, y)`: 20-35ns
* `x, y = t` (tuple expand): 10ns

Note that these results are very imprecise due to many factors, but
these should give a rough idea of the relative costs of various
operations.

Details: CPython 3.6.2, Macbook Pro 15" (Mid 2015), macOS Sierra
