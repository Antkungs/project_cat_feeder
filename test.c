#include <stdio.h>

int main() {
    char buffer[1024];
    fgets(buffer, sizeof(buffer), stdin);
    
    // ประมวลผลข้อมูล
    // ตัวอย่างง่าย ๆ จะส่งข้อมูลกลับเป็นตัวอักษรใน buffer
    printf("Received: %s\n", buffer);
    
    return 0;
}
