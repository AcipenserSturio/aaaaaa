#include <stdio.h>


#define uint8 unsigned char


// Makes four 6-bit packs from three bytes.
//
// Algorithm:
//     Input:  12345678 12345678 12345678
//     Output: 123456 781234 567812 345678
void make_four_packs_from_three_bytes(
        uint8* four_packs,
        const uint8* three_bytes
        ) {
    uint8 bit6_mask = (1 << 6) - 1;
    uint8 bit4_mask = (1 << 4) - 1;
    uint8 bit2_mask = (1 << 2) - 1;

    uint8 byte1_first6bits = three_bytes[0] >> 2;
    uint8 byte1_last2bits = three_bytes[0] & bit2_mask;

    uint8 byte2_first4bits = three_bytes[1] >> 4;
    uint8 byte2_last4bits = three_bytes[1] & bit4_mask;

    uint8 byte3_first2bits = three_bytes[2] >> 6;
    uint8 byte3_last6bits = three_bytes[2] & bit6_mask;

    four_packs[0] = byte1_first6bits;
    four_packs[1] = byte2_first4bits + (byte1_last2bits << 4);
    four_packs[2] = byte3_first2bits + (byte2_last4bits << 2);
    four_packs[3] = byte3_last6bits;
}


// Expands a 6-bit pack to a byte.
//
// Algorithm:
//     Prepend "01" to the given 6-bit pack respecting the leading zeros.
//     If the pack is "111111", prepend "00" instead (this exception exists
//     because "01111111" is a special delete character)
uint8 expand_pack_to_byte(uint8 pack) {
    if (pack == 63) {
        return pack;
    }

    return pack + 64;
}


// Makes four expanded bytes from four 6-bit packs using "expand_pack_to_byte"
// function.
void make_four_expanded_bytes_from_four_packs(
        uint8* four_expanded_bytes,
        const uint8* four_packs
        ) {
    for (uint8 i = 0; i < 4; ++i) {
        four_expanded_bytes[i] = expand_pack_to_byte(four_packs[i]);
    }
}


// Makes four expanded bytes from three raw bytes.
void make_four_expanded_bytes_from_three_bytes(
        uint8* four_expanded_bytes,
        const uint8* three_bytes
        ) {
    uint8 four_packs[4];

    make_four_packs_from_three_bytes(four_packs, three_bytes);
    make_four_expanded_bytes_from_four_packs(four_expanded_bytes, four_packs);
}


// Makes a digit character from a digit integer.
uint8 make_digit_char_from_digit_int(uint8 digit_int) {
    if (digit_int > 9) {
        printf("fatal: an attempt of converting an integer "
               "larger than 9 to an ASCII character\n");
        return 2;
    }
    return digit_int + 48;
}


int main(int argn, char* argv[]) {
    FILE* in;
    FILE* out;

    if (argn < 2) {
        printf("fatal: input file is not specified\n");
        return 1;
    } else if (argn == 2) {
        in = fopen(argv[1], "rb");
        out = fopen("transformed.txt", "wb");
    } else {
        in = fopen(argv[1], "rb");
        out = fopen(argv[2], "wb");
    }

    uint8 trail_fillers_count = 0;
    uint8 trail_fillers_count_char = make_digit_char_from_digit_int(0);

    // This is a placeholder for an actual value that will appear here later
    fwrite(&trail_fillers_count_char, 1, 1, out);

    while (1) {
        uint8 three_bytes[3];
        uint8 four_expanded_bytes[4];

        uint8 bytes_count = fread(three_bytes, 1, 3, in);

        if (bytes_count < 3) {
            if (bytes_count == 0) break;

            // These fillers at the end of the file allow us to be lazy, forget
            // about special cases and just use the algorithm below
            for (uint8 i = bytes_count; i < 3; ++i) {
                trail_fillers_count += 1;
                three_bytes[i] = 0;
            }
        }

        make_four_expanded_bytes_from_three_bytes(
                four_expanded_bytes,
                three_bytes);

        fwrite(four_expanded_bytes, 1, 4, out);
    }

    trail_fillers_count_char = make_digit_char_from_digit_int(
            trail_fillers_count);

    rewind(out);
    fwrite(&trail_fillers_count_char, 1, 1, out);

    return 0;
}
