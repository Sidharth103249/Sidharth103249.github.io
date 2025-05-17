#include<iostream>
using namespace std;
int a = 5;
int *ptr = &a;
int **pptr = &ptr;
int main(){
    cout << "Value of a is: " << a;
    cout << "Value of ptr is: " << ptr;
    cout << "Value of pptr is: " << **pptr;
}