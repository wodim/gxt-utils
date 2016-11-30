from collections import OrderedDict
import configparser
import struct
import sys

from utils import to_wchar


if len(sys.argv) < 3:
    print('Usage: %s <ini input> <gxt output>' % (sys.argv[0]))
    sys.exit(1)

config = configparser.ConfigParser()
config.read(sys.argv[1])
gxt_dict = OrderedDict(config['GXT'])
gxt_file = b''

# first we build the TDAT block
all_values = b''
current_offset, all_offsets = 0, []
for key, value in gxt_dict.items():
    all_offsets.append(current_offset)
    try:
        value = to_wchar(value)
    except KeyError as e:
        print('The following key has an unknown character: %s' % key.upper())
        raise
    all_values += value
    current_offset += len(value)
# char[4] "TDAT" + dword size + each value
tdat_size = len(all_values)
tdat_block = b'TDAT' + tdat_size.to_bytes(4, byteorder='little') + all_values

# now we build the TKEY block
# char[4] "TKEY" + dword size + each key (dword size + char[8] key)
tkey_size = len(gxt_dict) * (4 + 8)
all_keys = b''
for (key, value), offset in zip(gxt_dict.items(), all_offsets):
    key = bytearray(key.upper(), encoding='ascii')
    all_keys += struct.pack('<I8s', offset, key)
tkey_block = b'TKEY' + tkey_size.to_bytes(4, byteorder='little') + all_keys

gxt_file = tkey_block + tdat_block

with open(sys.argv[2], 'wb') as fp:
    fp.write(gxt_file)
