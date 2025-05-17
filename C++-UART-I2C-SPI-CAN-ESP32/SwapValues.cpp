#include<iostream>
using namespace std;
int a, b;
void swap(int* a, int* b)
{
    int x = *a;
    *a = *b;
    *b = x; 
}

int main()
{
    cout << "Input a";
    cin >> a;
    cout << "Input b";
    cin >> b;
    swap(&a,&b);
    cout << "Values of swapped a and b are:"<<"a: "<<a<<"b: "<<b;
    return 0;
}
