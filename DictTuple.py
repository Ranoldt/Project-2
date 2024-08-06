from mynamedtuple import mynamedtuple


class DictTuple:
    def __init__(self, *args):
        for arg in args:
            assert type(arg) is dict, f"{self.__class__.__name__}.__init__: {arg} is not a dictionary."
            assert len(arg) != 0, f"{self.__class__.__name__}.__init__: {arg} is empty."
        self.dt = list(args)

    def __len__(self):
        keys_set = {key for item in self.dt for key in item.keys()}
        return len(keys_set)

    def __bool__(self):
        if len(self.dt) > 1:
            return True
        return False


if __name__ == '__main__':
    coordinate = mynamedtuple('coordinate', 'x y')
    d = DictTuple({'c1': coordinate(1, 2)}, {'c1': coordinate(3, 4)})
    print(len(d))
    print(bool(d))