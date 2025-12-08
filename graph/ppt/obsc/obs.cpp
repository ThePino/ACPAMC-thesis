#include <stdio.h>

int main(int i) {
    return i < 13 && putchar("!dlrow olleh"[12 - i]) && main(++i);
}