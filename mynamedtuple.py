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
    init_method = f'    def init(self, {",".join(f'{name}= {value}' for name in field_names for value in default[name])}):\n'
    for name in field_names:
        init_method += f'        self.{name} = {name}\n'
