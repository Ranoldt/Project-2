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

    def __repr__(self):
        return f'{self.__class__.__name__}({", ".join(f'{item}' for item in self.dt)})'

    def __contains__(self, item):
        keys_set = {key for item in self.dt for key in item.keys()}
        return item in keys_set

    def __getitem__(self, key):
        for item in self.dt[::-1]:
            try:
                return item[key]
            except KeyError:
                continue
        else:
            raise KeyError(f"{key} is not in {self.dt}")

    def __setitem__(self, key, value):
        for item in self.dt[::-1]:
            if key in item:
                item[key] = value
                break
        else:
            self.dt.append({key: value})

    def __delitem__(self, key):
        deleted = False
        for item in self.dt[:]:
            if key in item:
                self.dt.remove(item)
                deleted = True

        if not deleted:
            raise KeyError(f"{key} is not in {self.dt}")


if __name__ == '__main__':
    coordinate = mynamedtuple('coordinate', 'x y')
    d = DictTuple({'c1': coordinate(1, 2)}, {'c1': coordinate(3, 4)})
    print(len(d))
    print(bool(d))
    print(d)
    if 'c2' in d:
        print('yea')
    else:
        print('no')
    print(d['c1'])
    d['c1'] = coordinate(2, 4)
    print('new:', d['c1'])
    d['c2'] = coordinate(1, 3)
    print(d.dt)
