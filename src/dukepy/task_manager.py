from multiprocessing import Process


def task1(args):
    print("task1")
    print(args)


def task2(args):
    print("task2")
    print(args)


def main():
    p1 = Process(target=task1, args=("hello",))
    p2 = Process(target=task2, args=("hello",))
    p1.start()
    p2.start()


if __name__ == "__main__":
    main()
