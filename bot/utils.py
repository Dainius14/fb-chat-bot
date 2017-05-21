def unicode_decode(string: str) -> str:
    result = ""
    for c in string:
        was_upper = c.isupper()
        c = c.lower()
        if c == 'ą':
            c = 'a'
        elif c == 'č':
            c = 'c'
        elif c == 'ę':
            c = 'e'
        elif c == 'ė':
            c = 'e'
        elif c == 'į':
            c = 'i'
        elif c == 'š':
            c = 's'
        elif c == 'ų':
            c = 'u'
        elif c == 'ū':
            c = 'u'
        elif c == 'ž':
            c = 'z'

        if was_upper: c = c.upper()
        result += c

    return result
