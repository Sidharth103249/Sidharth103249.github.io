#include<iostream>
using namespace std;
#define BUFFER_SIZE 8
char buffer[8];
char *read_ptr = buffer;
char *write_ptr = buffer;

void writedata(char data){
    *write_ptr = data;
    write_ptr++;
    if (write_ptr == buffer + BUFFER_SIZE){
        write_ptr = buffer;
    }

}
char read_data() {
    char data = *read_ptr;
    read_ptr++;
    if (read_ptr == buffer + BUFFER_SIZE) {
        read_ptr = buffer; // Wrap around
    }
    return data;
}
