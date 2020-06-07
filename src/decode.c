#include <stdio.h>

#define uint8 unsigned char


int main(int argn, char* argv[]) {
    FILE* in;
    FILE* out;

    if (argn < 2) {
        printf("fatal: input file is not specified\n");
        return 1;
    } else if (argn == 2) {
        in = fopen(argv[1], "rb");
        out = fopen("retransformed.txt", "wb");
    } else {
        in = fopen(argv[1], "rb");
        out = fopen(argv[2], "wb");
    }

    uint8 trail_fillers_count_char = 0;
    fread(&trail_fillers_count_char, 1, 1, in);

    uint8 trail_fillers_count = trail_fillers_count_char - 48;
    if (trail_fillers_count > 9) {
        printf("fatal: the input file is corrupted (a non-digit "
               "character is detected instead of the digit character "
               "of the trail fillers count\n");
        return 2;
    }


    while (1) {
        uint8 four_bytes[4];
        uint8 three_shrunk_bytes[3];

        uint8 bytes_count = fread(four_bytes, 1, 4, in);

        if (bytes_count < 4) {
            if (bytes_count == 0) break;

            printf("fatal: the input file is corrupted (the number "
                   "of bytes must be divisible by 4)\n");
            return 3;
        }

        uint8 shrunk_bytes_count = 3;

        // This construction detects EOF
        char c = getc(in);
        if (c == EOF) {
            shrunk_bytes_count = 3 - trail_fillers_count;
        }
        ungetc(c, in);

        uint8 bit6_mask = (1 << 6) - 1;
        uint8 bit4_mask = (1 << 4) - 1;
        uint8 bit2_mask = (1 << 2) - 1;

        uint8 pack1 = four_bytes[0] & bit6_mask;
        uint8 pack2 = four_bytes[1] & bit6_mask;
        uint8 pack3 = four_bytes[2] & bit6_mask;
        uint8 pack4 = four_bytes[3] & bit6_mask;

        uint8 pack1_6bits = pack1;
        uint8 pack2_first2bits = pack2 >> 4;
        uint8 pack2_last4bits = pack2 & bit4_mask;
        uint8 pack3_first4bits = pack3 >> 2;
        uint8 pack3_last2bits = pack3 & bit2_mask;
        uint8 pack4_6bits = pack4;

        three_shrunk_bytes[0] = (pack1_6bits << 2) + pack2_first2bits;
        three_shrunk_bytes[1] = (pack2_last4bits << 4) + pack3_first4bits;
        three_shrunk_bytes[2] = (pack3_last2bits << 6) + pack4_6bits;

        fwrite(three_shrunk_bytes, 1, shrunk_bytes_count, out);
    }

    return 0;
}
