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

    def __call__(self, key):
        value_lst = []
        for item in self.dt:
            if key in item:
                value_lst.append(list(item[key]._asdict().values()))
        return value_lst

    def __iter__(self):
        def gen_function(dt):
            keys_set = {key for item in dt[::-1] for key in sorted(list(item.keys()))}
            for key in keys_set:
                yield key
        return gen_function(self.dt)

    def __eq__(self, other):
        keys_set = {key for item in self.dt for key in item.keys()}
        if type(other) is DictTuple:
            for key in keys_set:
                if key not in other:
                    return False
                elif len(keys_set) != len(other):
                    return False
            return True
        elif type(other) is dict:
            if keys_set != set(other.keys()):
                return False
            elif len(keys_set) != len(other):
                return False
            return True

    def __add__(self, other):
        if type(other) is DictTuple:
            dt = self.dt + other.dt
            return DictTuple(*dt)
        elif type(other) is dict:
            dt = self.dt + [other]
            return DictTuple(*dt)
        else:
            raise TypeError(f"{other} is not a DictTuple or a dict")

    def __radd__(self, other):
        if type(other) is dict:
            dt = [other] + self.dt
            return DictTuple(*dt)
        else:
            raise TypeError(f"{other} is not a DictTuple or a dict")

    def __setattr__(self, key, value):
        try:
            if super().__getattribute__('dt'):
                dt_created = True
        except AttributeError:
            dt_created = False
            self.__dict__[key] = value
        if dt_created:
            raise AttributeError(f"Cannot Modify DictTuple attributes")


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
    print(d('c1'))
    for i in d:
        print(i)
    d1 = DictTuple({'c1': coordinate(1, 2)}, {'c1': coordinate(3, 4)})
    d2 = DictTuple({'c2': coordinate(1, 2)}, {'c3': coordinate(3, 4)})
    print(d2 + d1)
    adt = DictTuple({'c1': coordinate(1, 2)}, {'c1': coordinate(3, 4)})
    adict = {'c3': coordinate(3, 4)}
    print(adict + adt)


