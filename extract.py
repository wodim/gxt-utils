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

if tkey_block[0:4] != b'TKEY' or tdat_block[0:4] != b'TDAT':
    raise ValueError('Not a valid GXT file.')

tkey_keys = [x for x in struct.iter_unpack('<I8s', tkey_block[8:])]

gxt_dict = OrderedDict()
for offset, key in tkey_keys:
    key = key.decode('ascii').rstrip('\x00')

    value = b''
    while True:
        next = tdat_block[offset + 8:offset + 8 + 2]
        if next == b'\x00\x00':
            break
        value += next
        offset += 2
    gxt_dict[key] = from_wchar(value)

config = configparser.ConfigParser(interpolation=None)
config['GXT'] = gxt_dict

with open(sys.argv[2], 'w') as fp:
    config.write(fp)
