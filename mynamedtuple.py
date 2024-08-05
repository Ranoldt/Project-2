import keyword

def mynamedtuple(type_name, field_names, mutable = False, default = {}):
    assert type(type_name) is str and type_name[0].isalpha() == True and keyword.iskeyword(type_name) == False
    if type(field_names) is list:
        pass
    elif type(field_names) is str:
        if ',' in field_names:
            field_names = field_names.split(',','')
        else:
            field_names.split()
    else:
        raise SyntaxError("Fields must be a list or a string")

    for name in field_names:
        assert name[0].isalpha() == True and keyword.iskeyword(name) == False

    field_list = [element for element in field_names if element in list(default)]
    if len(field_list) != len(list(default)):
        raise SyntaxError("")

