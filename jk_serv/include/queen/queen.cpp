#include"queen.h"
#include "stdio.h"  
#include "stdlib.h" 
#define EXPORT __declspec(dllexport)
#include<iostream>
using namespace std;

DLLEXAMPLE_EXPORT_API int add(int a, int b)
{
	return a + b;
}


int foo(int a, int b)
{
	printf("you input %d and %d\n", a, b);
	return a + b;
}




class TestDLL {
public:
    void hello();
};
void TestDLL::hello() {
    cout << "hello world" << endl;
}



extern "C" {
    TestDLL td;
    EXPORT void hello() {
        td.hello();
    }

    EXPORT void hello1() {
        cout << "hello world 111111" << endl;
    }
}
