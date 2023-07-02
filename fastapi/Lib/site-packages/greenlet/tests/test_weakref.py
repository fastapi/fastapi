import gc
import weakref

import greenlet

from . import TestCase


class WeakRefTests(TestCase):
    def test_dead_weakref(self):
        def _dead_greenlet():
            g = greenlet.greenlet(lambda: None)
            g.switch()
            return g

        o = weakref.ref(_dead_greenlet())
        gc.collect()
        self.assertEqual(o(), None)

    def test_inactive_weakref(self):
        o = weakref.ref(greenlet.greenlet())
        gc.collect()
        self.assertEqual(o(), None)

    def test_dealloc_weakref(self):
        seen = []

        def worker():
            try:
                greenlet.getcurrent().parent.switch()
            finally:
                seen.append(g())

        g = greenlet.greenlet(worker)
        g.switch()
        g2 = greenlet.greenlet(lambda: None, g)
        g = weakref.ref(g2)
        g2 = None
        self.assertEqual(seen, [None])
