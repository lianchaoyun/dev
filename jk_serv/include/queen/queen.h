#pragma once
#include<iostream>
//���嵼��������DLLEXAMPLE_EXPORT_API�ں�������ǰ�������࣬����class������֮��
#define DLLEXAMPLE_EXPORT_API __declspec(dllexport)

DLLEXAMPLE_EXPORT_API int add(int a, int b);
