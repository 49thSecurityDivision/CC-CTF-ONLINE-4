#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define SIZE 200
#define GLOBAL 8

__thread long long global[1];

__attribute__((constructor)) void ignore_me() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
}

void get_flag(char* var, char* updated_var) {
  char* flag = getenv("FLAG");
  printf("%s\n", flag);

  return;
}

int main(void) {
  char answer[4] = { 0 };
  int size = 0;
  int c = 0;
  char updated_var[64] = { 0 };

  puts("I love local global variables...");
  puts("Will you update mine, please?");

  gets(answer);
  printf("You answered: ");
  printf(answer);
  puts("");

  if ('y' != answer[0]) {
    return 45;
  }

  printf("\nEnter the size of the new variable: ");
  scanf("%d", &size); // Size *must* be 6

  if (size > SIZE) {
    puts("\nWhoa... that is waaaay too many bytes...");
    return 255;
  }

  printf("\nEnter the new variable: ");
  while ((c = getchar()) != '\n' && c != EOF);
  gets(updated_var);

  puts("Updating the global variable...");
  for (int i = 0; i < 3; i++) {
    sleep(1);
  }

  puts("Just kidding... you don't get to define the variable...");

  for (int i = 0; i < 3; i++) {
    sleep(1);
  }

  puts("I DO!");

  global[size] = 0x4142434445464748;

  return 0;
}
