from mynamedtuple import mynamedtuple


class DictTuple:
    def __init__(self, *args):
        assert len(args) != 0, f"{self.__class__.__name__}.__init__: must have at least one argument"
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
        return f'{self.__class__.__name__}({", ".join(str(item) for item in self.dt)})'

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
                del item[key]
                if len(item) == 0:
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
            keys_lst = [key for item in dt[::-1] for key in sorted(list(item.keys()))]
            lst = []
            for key in keys_lst:
                if key not in lst:
                    lst.append(key)
                    yield key
        return gen_function(self.dt)

    def __eq__(self, other):
        if type(other) is DictTuple:
            other_set = {key for item in other.dt for key in item.keys()}
        elif type(other) is dict:
            other_set = {key for key in other.keys()}
        else:
            return False

        for key in other_set:
            if key not in self:
                return False
            if self[key] != other[key]:
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
        assert key == 'dt', f"DictTuple.__setattr__: {key} is not dt"
        if key not in self.__dict__:
            self.__dict__[key] = value
        else:
            raise AssertionError(f"DictTuple.__setattr__: cannot rebind attributes")













