import fire


class X():
    """
    Help X
    """

    def __init__(self):
        self.hello = "hello"

    def X_call(self):
        return "X_call"


class Y():
    """
    Help Y
    """

    def __init__(self):
        self.X = X


class Z():
    """
    Help Z
    """

    def __init__(self):
        self.Y = Y

    def Z_call(self, arg1=1, arg2=2, arg3=3):
        """
        Z call help
        :param arg1: To set arg1
        :param arg2: To set arg2
        :param arg3: To set arg3
        :return: a string "z_call"
        """
        return "Z_call"


if __name__ == "__main__":
    fire.Fire()
