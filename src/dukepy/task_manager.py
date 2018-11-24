from multiprocessing import Process, Event


class Task(Process):
    def __init__(self, *args, **kwargs):
        Process.__init__(self, *args, **kwargs)
        self._queue = []
        self._target = kwargs["target"]
        self._args = kwargs["args"]

    def run(self):
        self._target(*self._args)


def task1(args):
    print("task1")
    print(args)


def task2(args):
    print("task2")
    print(args)


def main():
    p1 = Task(target=task1, args=("hello",))
    p2 = Task(target=task2, args=("hello",))
    p1.start()
    p2.start()
    # p1.terminate()
    # p2.terminate()


if __name__ == "__main__":
    main()
