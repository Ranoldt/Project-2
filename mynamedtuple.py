import keyword


def mynamedtuple(type_name, field_names, mutable=False, default={}):
    # Validate type_name
    try:
        assert type(type_name) is str and type_name[0].isalpha() is True and keyword.iskeyword(type_name) is False
    except AssertionError:
        raise SyntaxError(f"Invalid type name: {type_name}")

    # Validate field name is list or string
    if type(field_names) is list:
        pass
    elif type(field_names) is str:
        if ',' in field_names:
            field_names = list(set(field_names.split(',')))
        else:
            field_names = list(set(field_names.split()))
    else:
        raise SyntaxError("Fields must be a list or a string")

    # Validate each field name
    for name in field_names:
        try:
            assert name[0].isalpha() is True and keyword.iskeyword(name) is False
        except AssertionError:
            raise SyntaxError(f"Invalid field name: {name}")

    # Check if all default fields are in field_names
    field_list = [element for element in field_names if element in list(default)]
    if len(field_list) != len(list(default)):
        raise SyntaxError("Mismatch between default fields and provided fields")

    # Class construction
    class_name = f'class {type_name}:\n'
    class_variables = f'    _fields = {field_names}\n'
    class_variables += f'    _mutable = {mutable}\n'

    # __init__ method
    init_method = f'    def __init__(self, {", ".join(f"{name}={default.get(name, None)}" for name in field_names)}):\n'
    for name in field_names:
        init_method += f'        self.{name} = {name}\n'

    # __repr__ method
    repr_method = '    def __repr__(self):\n'
    repr_method += f'        return f"{type_name}({", ".join(f"{name}={{self.{name}}}" for name in field_names)})"\n'

    # __getter__ methods
    get_methods = ''
    for name in field_names:
        get_methods += f'    def get_{name}(self):\n'
        get_methods += f'        return self.{name}\n'

    # __getitem__ method
    getitem_method = '    def __getitem__(self, index):\n'
    getitem_method += f'        return getattr(self, self._fields[index])\n'

    # __eq__ method
    eq_method = '    def __eq__(self, other):\n'
    eq_method += '        if type(self) is not type(other):\n'
    eq_method += '            return False\n'
    eq_method += '        elif self._fields != other._fields:\n'
    eq_method += '            return False\n'
    eq_method += '        for i in range(len(self._fields)):\n'
    eq_method += '            if self[i] != other[i]:\n'
    eq_method += '                return False\n'
    eq_method += '        return True\n'

    # _asdict method
    asdict_method = '    def _asdict(self):\n'
    asdict_method += '        return {key:self[i] for i,key in enumerate(self._fields)}\n'

    # _make method
    make_method = '    @classmethod\n'
    make_method += '    def _make(cls, iterable):\n'
    make_method += '        if type(iterable) is dict:\n'
    make_method += '            return cls(**iterable)\n'
    make_method += '        else:\n'
    make_method += '            return cls(*iterable)\n'

    # _replace method
    replace_method = '    def _replace(self, **kargs):\n'
    replace_method += '        if self._mutable:\n'
    replace_method += '            for key, value in kargs.items():\n'
    replace_method += '                setattr(self, key, value)\n'
    replace_method += '        else:\n'
    replace_method += '            param = {key: kargs.get(key, self._asdict().get(key)) for key in self._fields}\n'
    replace_method += f'            return self._make(param)\n'

    # __setattr__ method
    setattr_method = '    def __setattr__(self, name, value):\n'
    setattr_method += '        try:\n'
    setattr_method += '            val = super().__getattribute__(self._fields[-1])\n'
    setattr_method += '        except AttributeError:\n'
    setattr_method += '            self.__dict__[name] = value\n'
    setattr_method += '            return\n'
    setattr_method += '        if self._mutable:\n'
    setattr_method += '            self.__dict__[name] = value\n'
    setattr_method += '        else:\n'
    setattr_method += '            raise AttributeError("namedtuple is not mutable.")\n'

    class_def = class_name + class_variables + init_method + repr_method + get_methods + getitem_method
    class_def += eq_method + asdict_method + make_method + replace_method + setattr_method

    print(class_def)

    namespace = {}
    exec(class_def, {}, namespace)
    return namespace[type_name]


if __name__ == '__main__':
    coordinate = mynamedtuple('coordinate', 'x y', False, default={'y': 0})
    print(coordinate)
    origin = coordinate(0, 0)
    print(origin)
    origin.x = 1
    print(origin)

    """
    q1 - are you supposed to be able to add attributes
    q2 - does the _make method include strings as an iterable does it reflect. 
    """
