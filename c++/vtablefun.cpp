/*-------------------------------------------------------

@author NeverLost

Virtual table fun. 
Let's call VirtualTableHack::Print() directly from the vtable.

---------------------------------------------------------*/

#include <iostream>
#include <cstdint>

using std::cout;
using std::endl;
using std::uintptr_t;

class VirtualTableHack 
{
public:
    VirtualTableHack(int ctor_param) { param = ctor_param; }
    virtual void Print() { cout << "Object value: " << param << endl; }

private:
    int param;
};

int main()
{
    VirtualTableHack obj(1);

    // Print object value, result = 1
    obj.Print();

    // Virtual table pointer
    uintptr_t* vPointer = (uintptr_t*) &obj;
    vPointer = (uintptr_t*) *vPointer;

    // Call first function located in vTable, result = ??? undefined
    ((void (*)()) *vPointer)();
    
    // Why was the result undefined? The cast should work for normal functions.
    // True, but in this case we are dealing with a function that is associated with an object.
    // C++ hides this logic, but for every non-static function we have to pass a "this" variable.
    // This, so we can actually set the object's variables.

    // Call first function located in vTable and send obj as first param, result = 1
    ((void (*)(VirtualTableHack)) *vPointer)(obj);

    return 0;
}