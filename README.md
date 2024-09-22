mt make allows auto generate c/cpp makefile from a json config file

In a json file :
{
    "compilador": set the c/cpp compiler only: (gcc or g++) maybe clang,
    "fuentes": set the soources folder,
    "directorio_de_cabeceras": set your include path,
    "librerias": set the libs ,
    "directorio_del_ejecutable": set the output executable,
    "nombre": set the name of executable
}

Generating makefile:

python3 automake.py jsonfilename.json
