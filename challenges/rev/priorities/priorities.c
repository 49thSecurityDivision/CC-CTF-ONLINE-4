#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define INPUT 16

// TODO: Add a debug_printf function (dprintf)
unsigned int answer = 0;

void c0  (void) __attribute__((constructor (104)));
void c1  (void) __attribute__((constructor (105)));
void c2  (void) __attribute__((constructor (103)));
void c3  (void) __attribute__((constructor (106)));
void c4  (void) __attribute__((constructor (102)));
void c5  (void) __attribute__((constructor (108)));
void c6  (void) __attribute__((constructor (101)));
void c7  (void) __attribute__((constructor (107)));

__attribute__((constructor)) void ignore_me() {
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);
}

void c0(void) { // function 4
  for (int i = 0; i < 0xf; i++) {
    if (0 == answer) {
      answer = 0x1337;
    }

    answer += 0x1337;
    answer = (unsigned int)(answer / 2);
  }
  answer++;

  return;
}

void c1(void) { // function 5
  for (int i = 0; i < 0xfffff; i++) {
    answer--;
  }
  answer++;
  answer++;
  answer++;

  answer += 0x1337;

  return;
}

void c2(void) { // function 3
  for (int i = 0; i < 0xffff; i++) {
    answer--;
  }
  answer++;
  answer--;
  answer++;
  answer--;
  answer--;
  answer--;
  answer++;
  answer--;
  
  answer += 0x1337;

  return;
}

void c3(void) { // function 6
  answer = (int)(answer / 2);

  answer += 0x1337;

  return;
}

void c4(void) { // function 2
  answer *= 4;

  answer += 0x1337;

  return;
}

void c5(void) { // function 8
  answer *= 1;
  answer--;
  answer++;
  answer++;
  answer++;
  answer++;
  answer++;
  answer++;
  answer++;

  answer += 0x1337;

  return;
}

void c6(void) { // function 1
  char* chr_answer = NULL;
  chr_answer = getenv("ANSWER");
  if (NULL == chr_answer) {
    exit(0x30);
  } else {
    answer = atoi(chr_answer);
    chr_answer = NULL;
  }

  if (0 == answer) {
    exit(0x32);
  }

  answer += 0x1337;

  return;
}

void c7(void) { // function 7
  answer >>= 0x8;

  answer += 0x1337;

  return;
}

int main(void) {
  srand(answer);

  unsigned int guess = 0;
  char input[INPUT] = { 0 };

  printf("What is the answer: ");
  fgets(input, INPUT, stdin);

  guess = atoi((const char*)input);
  printf("GUESS: %d\n", guess);

  guess ^= answer;

  printf("POST XOR: 0x%08x\n", guess);

  if (guess == 0x7672306e) {
    char* flag = getenv("FLAG");
    printf("Wow... you sure know your priorities\n");
    printf("%s\n", flag);
  } else {
    printf("Nice try...\n");
  }

  return 0;
}
