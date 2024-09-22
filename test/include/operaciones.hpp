#pragma once
#include <thread>
#include <vector>
class Vector{
    public:
        int x,y;
        Vector(int x,int y);
        Vector operator+(Vector opt);
        Vector operator-(Vector opt);
};