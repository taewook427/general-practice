import ctypes

c_module = ctypes.windll.LoadLibrary('.\\test290.dll')

add = c_module.add
add.argtypes = (ctypes.c_int, ctypes.c_int)
add.restype = ctypes.c_int

print( add(23,77) )

'''
#include "pch.h"

extern "C"
{
    // 1. int 타입 인자를 받고, int 타입을 리턴하는 예
    __declspec(dllexport) int add(int a, int b)
    {
        return a + b;
    }

}
'''
