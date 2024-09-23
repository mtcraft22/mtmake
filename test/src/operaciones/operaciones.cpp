#include <operaciones.hpp>


Vector::Vector(int x, int y):x(x),y(y){}
Vector Vector::operator+(Vector opt){
    return Vector(this->x + opt.x, this->y+opt.y);
}
Vector Vector::operator-(Vector opt){
    return Vector(this->x - opt.x, this->y-opt.y);
}