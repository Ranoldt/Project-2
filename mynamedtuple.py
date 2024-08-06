import keyword


def mynamedtuple(type_name, field_names, mutable=False, default={}):
    try:
        assert type(type_name) is str and type_name[0].isalpha() is True and keyword.iskeyword(type_name) is False
    except AssertionError:
        raise SyntaxError(f"Invalid type name: {type_name}")

    if type(field_names) is list:
        pass
    elif type(field_names) is str:
        if ',' in field_names:
            field_names = field_names.split(',')
        else:
            field_names = field_names.split()
    else:
        raise SyntaxError("Fields must be a list or a string")

    for name in field_names:
        try:
            assert name[0].isalpha() is True and keyword.iskeyword(name) is False
        except AssertionError:
            raise SyntaxError(f"Invalid field name: {name}")

    field_list = [element for element in field_names if element in list(default)]
    if len(field_list) != len(list(default)):
        raise SyntaxError("Mismatch between default fields and provided fields")

    class_name = f'class {type_name}:\n'
    class_variables = f'    _fields = {field_names}\n'
    class_variables += f'    _mutable = {mutable}\n'

    init_method = f'    def __init__(self, {", ".join(f"{name} = {default.get(name)}" for name in field_names)}):\n'
    for name in field_names:
        init_method += f'        self.{name} = {name}\n'

    repr_method = f'    def __repr__(self):\n'
    repr_method += f'        return f"{type_name}({", ".join(f"{name}={{self.{name}}}" for name in field_names)})"\n'

    get_methods = ''
    for name in field_names:
        get_methods += f'    def get_{name}(self):\n'
        get_methods += f'        return self.{name}\n'

    getitem_method = '    def __getitem__(self, index):\n'
    getitem_method += f'        return getattr(self, self._fields[index])\n'

    eq_method = '    def __eq__(self, other):\n'
    eq_method += '        if type(self) is not type(other):\n'
    eq_method += '            return False\n'
    eq_method += '        elif self._fields != other._fields:\n'
    eq_method += '            return False\n'
    eq_method += '        elif self._fields != other._fields:\n'
    eq_method += '            return False\n'
    eq_method += '        for i in range(len(self._fields)):\n'
    eq_method += '            if self[i] != other[i]:\n'
    eq_method += '                return False\n'
    eq_method += '        return True\n'

    asdict_method = '    def _asdict(self):\n'
    asdict_method += '        return {key:self[i] for i,key in enumerate(self._fields)}\n'

    make_method = '    @classmethod\n'
    make_method += '    def _make(cls, iterable):\n'
    make_method += '        return cls(*iterable)\n'

    class_def = class_name + class_variables + init_method + repr_method + get_methods + getitem_method + eq_method
    class_def += asdict_method + make_method

    print(class_def)
    namespace = {}
    exec(class_def, {}, namespace)
    return namespace[type_name]


if __name__ == '__main__':
    coordinate = mynamedtuple('coordinate', 'x y', default={'y': 0})
    print(coordinate)
    coord = coordinate(1, 2)
    coord1 = coordinate(2, 2)

    print(coord == coord1)
