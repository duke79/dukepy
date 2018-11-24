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
            while not self._events[self._predecessor.uid].is_set():
                pass

        self._target(*self._args)
        self._events[self.uid].set()

    def terminate(self):
        self._events[self.uid].set()
        Process.terminate(self)

    def run_after(self, p):
        self._predecessor = p


def task_cb(args):
    print(args)


def main():
    p1 = Task(target=task_cb, args=("task1",))
    p2 = Task(target=task_cb, args=("task2",))
    p3 = Task(target=task_cb, args=("task3",))
    p1.run_after(p2)
    p2.run_after(p3)
    p1.start()
    p2.start()
    p3.start()
    # p1.terminate()
    p2.terminate()


if __name__ == "__main__":
    main()
