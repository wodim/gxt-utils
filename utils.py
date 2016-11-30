gxt_charset = tuple(
    '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    '\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
    " !△#$%&'()*+,-./0123456789:;◀=▶?"
    '™ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_'
    '`abcdefghijklmnopqrstuvwxyz❤○ ~ '
    'ÀÁÂÄÆÇÈÉÊËÌÍÎÏÒÓÔÖÙÚÛÜßàáâäæçèéê'
    'ëìíîïòóôöùúûüÑñ¿¡´              '
    '                                '
    '                                '
)


def from_wchar(wchar_str):
    ret = ''
    for character in (wchar_str[i:i + 2] for i in range(0, len(wchar_str), 2)):
        index = int.from_bytes(character, byteorder='little')
        ret += gxt_charset[index]
    return ret


def to_wchar(input_str):
    ret = b''
    for character in input_str:
        index = gxt_charset.index(character)
        ret += index.to_bytes(2, byteorder='little')
    ret += b'\x00\x00'
    return ret
