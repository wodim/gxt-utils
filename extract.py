from collections import OrderedDict
import configparser
import struct
import sys

from utils import from_wchar


if len(sys.argv) < 3:
    print('Usage: %s <gxt input> <ini output>' % (sys.argv[0]))
    sys.exit(1)

gxt_contents = open(sys.argv[1], 'rb').read()

tkey_block_size = int.from_bytes(gxt_contents[4:8], byteorder='little') + 8
tkey_block = gxt_contents[:tkey_block_size]
tdat_block = gxt_contents[tkey_block_size:]

assert tkey_block[0:4] == b'TKEY'
assert tdat_block[0:4] == b'TDAT'

tkey_keys = [x for x in struct.iter_unpack('<I8s', tkey_block[8:])]

gxt_dict = OrderedDict()
for offset, key in tkey_keys:
    offset += 8
    key = key.decode('ascii').rstrip('\x00')

    value = b''
    while tdat_block[offset:offset + 2] != b'\x00\x00':
        value += tdat_block[offset:offset + 2]
        offset += 2

    gxt_dict[key] = from_wchar(value)

config = configparser.ConfigParser(interpolation=None)
config['GXT'] = gxt_dict

with open(sys.argv[2], 'w') as fp:
    config.write(fp)
