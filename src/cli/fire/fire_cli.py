import fire


def another_really_do_something(with_a_twist=False):
    """
    another_really_do_something help
    :param with_a_twist:
    :return:
    """

    if with_a_twist:
        return "doing something with a twist"
    return "doing something"

class ObjToDoSomething():
    """
    ObjToDoSomething help
    """

    def really_do_something(self, with_a_twist=False):
        """
        really do something help
        :param with_a_twist:
        :return:
        """

        if with_a_twist:
            return "doing something with a twist"
        return "doing something"


class RootCmd():
    """This is THE cli"""
    do_something_else = "doing something else"

    def __init__(self, init_like=10):
        self.do_something_else_entirely = "doing something else entirely"
        self.initialized_like = init_like

    def do_something(self):
        """
        do something help
        :return:
        """
        return ObjToDoSomething

    def another_do_something(self):
        """
        another_do_something help
        :return:
        """
        return another_really_do_something()


if __name__ == "__main__":
    fire.Fire(RootCmd)
