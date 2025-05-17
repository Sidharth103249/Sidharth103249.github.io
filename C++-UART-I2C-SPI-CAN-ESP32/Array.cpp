#include<iostream>
using namespace std;
void myFunction(int array[20])
{
    cout << "Size of array after passing is: " << sizeof(array);
}

int main()
{
    int myArray[20];
    myFunction(myArray);
    // cout << "Values of swapped a and b are:"<<"a: "<<a<<"b: "<<b;
    return 0;
}
