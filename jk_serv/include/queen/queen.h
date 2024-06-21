#pragma once
#include<iostream>
//定义导出函数，DLLEXAMPLE_EXPORT_API在函数类型前，若是类，则在class和类名之间
#define DLLEXAMPLE_EXPORT_API __declspec(dllexport)

DLLEXAMPLE_EXPORT_API int add(int a, int b);
