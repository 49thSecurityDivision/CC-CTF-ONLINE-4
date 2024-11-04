#include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 
#include <unistd.h> 

void complicate2(unsigned char* ret) {
  int r = rand();
  r &= 0xff000000;
  r >>= 24;

  *ret ^= (unsigned char)r;
}

void complicate1(unsigned char* ret) {
  int r = rand();
  r &= 0x0000ff00;
  r >>= 8;

  *ret ^= (unsigned char)r;

  complicate2(ret);
}

unsigned char algo(unsigned char c, unsigned char r) {
  unsigned char ret = '\0';
  ret = c ^ r;

  complicate1(&ret);

  return ret;
}

unsigned char compute_char(unsigned char src, unsigned char* seed) {
  *seed = algo(src, *seed);

  return *seed;
}

void compute_flag(char* buf, unsigned char* result) {
  unsigned char val = '\0';

  int i = 0;
  unsigned char seed = '\xff';

  srand(0b01110011);

  for (; i < strlen(buf); i++) {
    val = compute_char((unsigned char)buf[i], &seed);
    result[i] = val;
  }
}

void get_flag() {
  char buf[512] = { 0 };
  unsigned char result[512] = { 0 };
  int bytes = read(0, buf, 512);

  buf[bytes] = '\0';
  compute_flag(buf, result);
  
  for (int i = 0; i < strlen(result); i++) {
    printf("%02x", result[i]);
  }
  puts("");
}

int main(void) {
  get_flag();
}
