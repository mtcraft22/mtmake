Include = -I../include 
libpath = ../lib
objects = $(shell ls ./*.o)
operaciones.o:../src/operaciones/operaciones.cpp
	g++-12 -c ../src/operaciones/operaciones.cpp -fPIC $(Include)
all:operaciones.o 
	g++-12 -shared -fPIC -o ../lib/libvectores.so $(objects) $(lib)
Include = -I../include 
lib = -lvectores 
libpath = ../lib
objects = $(shell ls ./*.o)
hola.o:../src/hola.cpp
	g++-12 -c ../src/hola.cpp -fPIC $(Include)
all:hola.o 
	g++-12 -o ../release/vectores $(objects) $(lib)
clear:
	rm -r $(objects)
