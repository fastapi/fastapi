from greenlet import greenlet

from . import TestCase


class genlet(greenlet):
    parent = None

    def __init__(self, *args, **kwds):
        self.args = args
        self.kwds = kwds

    def run(self):
        (fn,) = self.fn
        fn(*self.args, **self.kwds)

    def __iter__(self):
        return self

    def __next__(self):
        self.parent = greenlet.getcurrent()
        result = self.switch()
        if self:
            return result

        raise StopIteration

    next = __next__


def Yield(value):
    g = greenlet.getcurrent()
    while not isinstance(g, genlet):
        if g is None:
            raise RuntimeError("yield outside a genlet")
        g = g.parent
    g.parent.switch(value)


def generator(func):
    class Generator(genlet):
        fn = (func,)

    return Generator


# ____________________________________________________________


class GeneratorTests(TestCase):
    def test_generator(self):
        seen = []

        def g(n):
            for i in range(n):
                seen.append(i)
                Yield(i)

        g = generator(g)
        for _ in range(3):
            for j in g(5):
                seen.append(j)
        self.assertEqual(seen, 3 * [0, 0, 1, 1, 2, 2, 3, 3, 4, 4])
