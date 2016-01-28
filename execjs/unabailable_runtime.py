import execjs


class UnavailableRuntime:
    def __init__(self, name):
        self.name = name

    def exec_(self, source):
        raise execjs.RuntimeError

    def eval(self, source):
        raise execjs.RuntimeError

    def compile(self, source):
        raise execjs.RuntimeError

    def is_available(self):
        return False
