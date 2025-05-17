#include<iostream>
using namespace std;
#define BUFFER_SIZE 8
class RingBufferOnHeap
{
private:
    char *buffer;
    char *read_ptr;
    char *write_ptr;
    int count;

public:
    RingBufferOnHeap(){
        buffer = new char[BUFFER_SIZE];
        read_ptr = buffer;
        write_ptr = buffer;
        count = 0;
    }
    ~RingBufferOnHeap(){
        delete[] buffer;
    }
    bool read(char &data){
         if(count == 0) {
            cout << "Buffer read. Cannot read:" << endl;
            return false;
        }
        data = *read_ptr;
        read_ptr++;
        if(read_ptr == buffer + BUFFER_SIZE) {
            read_ptr = buffer;
        }
        count--;
        return true;
    }

    bool write(char data){
        if(count == BUFFER_SIZE) {
            cout << "Buffer full. Cannot write:" << data;
            return false;
        }
        *write_ptr = data;
        write_ptr++;
        if(write_ptr == buffer + BUFFER_SIZE) {
            write_ptr = buffer;
        }
        count++;
        return true;
    }

    void print_status(){
        cout << "The current count is: " << count << endl;
    }
};

int main(){
    RingBufferOnHeap Rb;
    Rb.write('A');
    Rb.write('B');
    Rb.write('C');
    Rb.write('D');
    Rb.write('E');
    Rb.write('F');
    Rb.write('G');
    Rb.write('H');
    Rb.print_status();
    Rb.write('I');
    char out;
        while (Rb.read(out)) {
        cout << "Read: " << out << endl;
    }
    Rb.read(out);
    return 0;
}

