#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char alph[90] = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+,-./:;<=>?@^_`{|}~\0";

unsigned char compute_char(unsigned char src, unsigned char* seed) {
  int r1 = rand();
  r1 &= 0x0000ff00;
  r1 >>= 8;
  int r2 = rand();
  r2 &= 0xff000000;
  r2 >>= 24;

  *seed = src ^ *seed ^ (unsigned char)r1 ^ (unsigned char)r2;

  return *seed;
}

int main(void) {
  char buf[50] = { 0 };
  unsigned char result[50] = "\xfd\x85\x50\xac\xbb\xeb\xa5\x40\x9a\x7d\xab\x76\x0f\xc2\xd7\xca\x2f\x90\xbf\x72\x08\xa0\x1a\x67\x85\x1b\x75\xfc\x55\x48\xa1\xa5\x3e\x70\0";


  unsigned char val = '\0';
  unsigned char seed = '\xff';
  int index = 0;

  for (int k = 0; k < strlen(alph); k++) {
    srand(0b01110011);
    seed = '\xff';
    buf[index] = alph[k];
    for (int j = 0; j < strlen(buf); j++) {
      val = compute_char((unsigned char)buf[j], &seed);
    }
    if (val == result[index]) {
      printf("buf: %s\n", buf);
      k = -1; // loop increments this to 0
      index++;
    }
  }

  return 0;
}
