import sys

if len(sys.argv) < 2:
    input_filename = 'transformed.txt'
else:
    input_filename = sys.argv[1]

f = open(input_filename, 'rb')

transformed_back = bytes()
trail_len = f.read(1)[0] - ord('0')

while True:
    # read pack of 8 bytes
    pack_bytes = f.read(8)
    # print(pack_bytes, end = ' ')
    if len(pack_bytes) == 0:
        break
    if len(pack_bytes) != 8:
        raise Exception("Ummm file does not have proper size m8")
    pack_bits = int.from_bytes(pack_bytes, 'big') # array -> bits

    # compress each 8-bit char back to being 6 bits of a byte
    result = 0
    for i in range(8):
        byte = pack_bytes[7-i]
        if byte < 0x3f or byte > 0x7e:
            raise Exception("Ummm file contains invalid chars m8")
        if (byte != 63):  # \x7f escape
            byte -= (1 << 6)
        byte <<= 6 * i
        result += byte
    # print(result.to_bytes(6, 'big'))
    transformed_back += result.to_bytes(6, 'big')

f.close()

if len(sys.argv) < 3:
    result_filename = 're_transformed'
else:
    result_filename = sys.argv[2]

f = open(result_filename, 'bw')
f.write(transformed_back[:-trail_len])
f.close()
