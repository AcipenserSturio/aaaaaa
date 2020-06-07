import sys

f = open(sys.argv[1], 'rb')

transformed = bytes()
trail_len = 0
while True:
    # read pack of 6 bytes
    pack_bytes = f.read(6)
    # print(pack_bytes, end = ' ')
    if len(pack_bytes) == 0:
        break
    pack_bits = int.from_bytes(pack_bytes, 'big')
    if len(pack_bytes) < 6:
        # add trailing zeros, we will throw them out when decoding
        trail_len = 6 - len(pack_bytes)
        pack_bits <<= trail_len*8

    # expand every 6 bits to 8-bit ascii char (displayable)
    mask = (1 << 6) - 1
    result = 0
    for i in range(8):
        byte = pack_bits & (mask << 6*i)
        byte >>= 6*i
        if (byte != 63):  # \x7f escape
            byte += (1 << 6)
        byte <<= 8*i
        result += byte
    # print(result.to_bytes(8, 'big'))
    transformed += result.to_bytes(8, 'big')
f.close()

if len(sys.argv) < 3:
    result_filename = 'transformed.txt'
else:
    result_filename = sys.argv[2]

f = open(result_filename, 'bw')

# add amount of trailing zeroed bytes
f.write(bytes([trail_len + ord('0')]))
f.write(transformed)
f.close()

