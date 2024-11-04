#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 4

char global[SIZE] = { 0 };

__attribute__((constructor)) void ignore_me() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
}

void there_is_no_need_get_angry() {
  __asm__("push %rdi");
  __asm__("ret");
  __asm__("pop %rdi");
  __asm__("ret");
  __asm__("push %rsi");
  __asm__("ret");
  __asm__("pop %rsi");
  __asm__("ret");
  __asm__("push %rdx");
  __asm__("ret");
  __asm__("pop %rdx");
  __asm__("ret");
}

void solve() {
  char* flag = getenv("FLAG");

  for (int i = 0; i < SIZE; i++) {
    if (0x0 == global[i]) {
      exit(0x55);
    }
  }

  printf("%s\n", flag);
  
  return;
}

void func0(int arg1, int arg2, int arg3) { // 1, 1073774590, 1
  global[0] = 'f';

  if (((arg1 + arg2) * arg3) == 4096)
    global[0] = '\0';

  if ((arg3 >> 2) > 4096)
    global[0] = '\0';

  if ((arg2 << 2) < 4096)
    global[0] = '\0';

  if ((arg1 - arg3) > 0)
    global[0] = '\0';

  if (arg1 > (arg2 + arg3))
    global[0] = '\0';

  if (arg1 == 0)
    global[0] = '\0';

  if (arg2 == 0)
    global[0] = '\0';

  if (arg3 == 0)
    global[0] = '\0';

  return;
}

void func1(int arg1, int arg2) { // 3, 392
  global[1] = 'l';

  if (arg1 > arg2)
    global[1] = '\0';

  if ((arg1 * arg2) < 1024)
    global[1] = '\0';

  if ((arg1 + arg2 + 100) > 500)
    global[1] = '\0';

  if (arg1 == 0)
    global[1] = '\0';

  if (arg2 == 0)
    global[1] = '\0';

end:
  return;
}

void func2(int arg1) { // 4293980400
  global[2] = 'a';

  if (arg1 < 0xff000000)
    global[2] = '\0';

  if ((arg1 & 0xf0f0f0f0) >> 4 < 0x0f0f0f0f)
    global[2] = '\0';

  if (((arg1 - 2) & 2) != 2)
    global[2] = '\0';

  if (arg1 & 2 != 0)
    global[2] = '\0';

  return;
}

void func3(int arg1, int arg2, int arg3) { // 2653980557 3850270113 2417962352
  global[3] = 'g';

  if (((((arg1 * arg3) >> arg1) - arg2) + arg3) * arg1 < ((arg1 << arg2) + arg3) * 32)
    global[3] = '\0';

  if (arg1 == 0)
    global[3] = '\0';

  if (arg2 == 0)
    global[3] = '\0';

  if (arg3 == 0)
    global[3] = '\0';

  return;
}

int main(int argc, char** argv) {
  puts("What motivates you?");
  char whatever[SIZE] = { 0 };
  fgets(whatever, 1024, stdin);

  if (0 == strncmp("angr", whatever, SIZE)) {
    puts("I AGREE!");
  } else {
    puts("We are not the same...");
  }

  puts("Goodbye...");

  return 0;
}
