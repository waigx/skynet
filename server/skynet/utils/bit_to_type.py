def bits_to_type(i):
    x = i
    result = []
    type_dict = {
        0: '',
        1: 'First Name',
        2: 'Last Name',
        4: 'Birth Date',
        8: 'Email',
        16: 'Address',
        32: 'Phone'
    }
    while i > 0 and x < 64:
        x = i & (-i)
        i -= x
        result += [type_dict[x]]
    return ', '.join(result)
