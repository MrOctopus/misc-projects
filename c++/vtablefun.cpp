/*-------------------------------------------------------

@author NeverLost

Virtual table fun. 
Let's call Test::hey() directly from the vtable.

---------------------------------------------------------*/

#include <iostream>
#include <cstdint>

using namespace std;

class Test 
{
public:
    int ignore;
    virtual void hey() { cout << "\nHey\n"; }
};

int main()
{
    Test obj;
    uintptr_t* pointer = (uintptr_t*) &obj;
    pointer = (uintptr_t*) *pointer;
    (void (*)()) *pointer)();
    return 0;
}