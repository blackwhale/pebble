import unittest
try:  # Python 2
    from Queue import Queue
except:  # Python 3
    from queue import Queue

from pebble import thread


@thread.concurrent(name='foo')
def function(queue, argument, keyword_argument=0):
    """A docstring."""
    queue.put(argument + keyword_argument)


class TestThreadConcurrentObj(object):
    a = 0

    def __init__(self):
        self.b = 1

    @classmethod
    @thread.concurrent
    def clsmethod(cls, queue):
        queue.put(cls.a)

    @thread.concurrent
    def instmethod(self, queue):
        queue.put(self.b)

    @staticmethod
    @thread.concurrent
    def stcmethod(queue):
        queue.put(2)


class TestThreadConcurrent(unittest.TestCase):
    def setUp(self):
        self.concurrentobj = TestThreadConcurrentObj()

    def test_docstring(self):
        """Thread Concurrent docstring is preserved."""
        self.assertEqual(function.__doc__, "A docstring.")

    def test_thread_wrong_decoration(self):
        """Thread Concurrent raises ValueError if given wrong params."""
        try:
            @thread.concurrent(5)
            def wrong():
                return
        except Exception as error:
            self.assertTrue(isinstance(error, ValueError))

    def test_defaults(self):
        """Thread Concurrent default values are preserved."""
        queue = Queue()
        thrd = function(queue, 1, 1)
        thrd.join()
        self.assertFalse(thrd.daemon)

    def test_arguments(self):
        """Thread Concurrent decorator arguments are forwarded."""
        queue = Queue()
        thrd = function(queue, 1, 1)
        thrd.join()
        self.assertEqual(thrd.name, 'foo')

    def test_function_results(self):
        """Thread Concurrent results are produced."""
        queue = Queue()
        thrd = function(queue, 1, 1)
        results = queue.get()
        thrd.join()
        self.assertEqual(results, 2)

    def test_class_method(self):
        """Thread Concurrent decorated classmethods."""
        queue = Queue()
        thrd = TestThreadConcurrentObj.clsmethod(queue)
        results = queue.get()
        thrd.join()
        self.assertEqual(results, 0)

    def test_instance_method(self):
        """Thread Concurrent decorated instance methods."""
        queue = Queue()
        thrd = self.concurrentobj.instmethod(queue)
        results = queue.get()
        thrd.join()
        self.assertEqual(results, 1)

    def test_static_method(self):
        """Thread Concurrent decorated static methods."""
        queue = Queue()
        thrd = self.concurrentobj.stcmethod(queue)
        results = queue.get()
        thrd.join()
        self.assertEqual(results, 2)