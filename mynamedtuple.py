import keyword

def mynamedtuple(type_name, field_names, mutable = False, default = {}):
    try:
        assert type(type_name) is str and type_name[0].isalpha() == True and keyword.iskeyword(type_name) == False
    except AssertionError:
        raise SyntaxError(f"Invalid type name: {type_name}")

    if type(field_names) is list:
        pass
    elif type(field_names) is str:
        if ',' in field_names:
            field_names = field_names.split(',','')
        else:
            field_names.split()
    else:
        raise SyntaxError("Fields must be a list or a string")

    try:
        for name in field_names:
            assert name[0].isalpha() == True and keyword.iskeyword(name) == False
    except AssertionError:
        raise SyntaxError(f"Invalid field name: {name}")

    field_list = [element for element in field_names if element in list(default)]
    if len(field_list) != len(list(default)):
        raise SyntaxError("Mismatch between default fields and provided fields")

    class_name = f'class {type_name}:\n'
    init_method = f'    def init(self, {", ".join(f"{name} = {default.get(name)}" for name in field_names)}):\n'
    for name in field_names:
        init_method += f'        self.{name} = {name}\n'

    repr_method = f'    def repr(self):\n'
    repr_method += f'        return f"{type_name}({", ".join(f"{name}={{self.{name}!r}}" for name in field_names)})"\n'

    get_methods = ''
    for name in field_names:
        get_methods += f'    def get{name}(self):\n'
        get_methods += f'        return self.{name}\n'

    class_def = class_name + init_method + repr_method
    print(class_def)