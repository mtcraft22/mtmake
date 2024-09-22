
#include <iostream>
#include <operaciones.hpp>
#include <ostream>


int main(int argc, char** argv){
    Vector a = Vector(10,10);
    Vector b = Vector(20,20);
    std::cout << (a+b).x << std::endl;
    return 0;
}