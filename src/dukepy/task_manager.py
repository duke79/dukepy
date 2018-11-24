import uuid
from multiprocessing import Process, Event

from dukepy.singleton import Singleton


class Ledger(metaclass=Singleton):
    all_tasks = []
    events = {}


class Task(Process):
    def __init__(self, *args, **kwargs):
        Process.__init__(self, *args, **kwargs)
        Ledger().all_tasks.append(self)

        self._predecessor = None
        self.uid = uuid.uuid4()

        Ledger().events[self.uid] = Event()
        self._events = Ledger().events  # Keeping a copy ro access in Run()

        self._target = kwargs["target"]
        self._args = kwargs["args"]

    def run(self):
        if self._predecessor:
            while not self._events[self._predecessor].is_set():
                pass

        self._target(*self._args)
        self._events[self.uid].set()

    def run_after(self, p):
        self._predecessor = p


def task1(args):
    print("task1")
    print(args)


def task2(args):
    print("task2")
    print(args)


def main():
    p1 = Task(target=task1, args=("hello",))
    p2 = Task(target=task2, args=("hello",))
    p1.run_after(p2.uid)
    p1.start()
    p2.start()
    # p1.terminate()
    # p2.terminate()


if __name__ == "__main__":
    main()
