import json
import sys
import os
import platform

class Make:
    def __init__(self , data):
        self.compilador:str =                data["compilador"]
        self.fuentes:str =                   data["fuentes"]
        self.directorio_de_cabeceras:str =   data["directorio_de_cabeceras"]
        self.librerias:str =                 data["librerias"]
        self.directorio_de_ejecutable:str =  data["directorio_del_ejecutable"]
        self.nombre:str =                    data["nombre"]
        self.tipo:str =                      data["tipo"]
        self.opciones:str =                  data["opciones"]
        self.__output =                    []
    def __declare_var(self,name,value):
        self.__output.append(name + " = " +value)
    def __declare_rule(self,name,dependecies:list[str],commands:list[str]):
        dp = ""
        for i in dependecies:
            dp += i + " "
        self.__output.append(name + ":" + dp)
        for j in commands:
            self.__output.append(i)
    def __compile(self,file,options):
        self.__declare_rule("all",file,f"{self.compilador} -c {file} {options} $(Include)")
    def __link(self,type):
        match type:
            case "shared":
                match platform.system():
                    case "Linux":
                        self.__declare_rule("all","$(objects)",f"{self.compilador} -shared {self.directorio_de_ejecutable}/lib{self.nombre}.so $(objects) $(lib)")
                    case "Windows":
                        self.__declare_rule("all","$(objects)",f"{self.compilador} -shared {self.directorio_de_ejecutable}/lib{self.nombre}.dll $(objects) $(lib)")
                    case "Darwin":
                        self.__declare_rule("all","$(objects)",f"{self.compilador} -shared {self.directorio_de_ejecutable}/lib{self.nombre}.dylib $(objects) $(lib)")
                    case _:
                        raise ValueError("This platform is not suported")
            case "static":
                
               
                self.__declare_rule(
                    "all",
                    "$(objects)",
                    f"ar rcs {self.nombre}.a  $(objects)"
                )
            case "app":
                match platform.system():
                    case "Linux":
                        self.__declare_rule("all","$(objects)",f"{self.compilador} -o {self.directorio_de_ejecutable}/{self.nombre} $(objects) $(lib)")
                    case "Windows":
                        self.__declare_rule("all","$(objects)",f"{self.compilador} -o {self.directorio_de_ejecutable}/{self.nombre}.exe $(objects) $(lib)")
                    case "Darwin":
                        self.__declare_rule("all","$(objects)",f"{self.compilador} -o {self.directorio_de_ejecutable}/{self.nombre} $(objects) $(lib)")
                    case _:
                        raise ValueError("This platform is not suported")
            case _:
                raise ValueError("Option not suported")
    def make_make(self):
        inc = ""
        for i in self.directorio_de_cabeceras.split(" "):
            inc += ("-I"+i)+" "
        self.__declare_var("Include",inc)
        lib = ""
        for j in self.librerias.split(" "):
            if j.endswith(".a"):
                lib += j + " "
            else:
                lib += "-l"+j+" "
        self.__declare_var("lib",lib)
        self.__declare_var("objects", "$(shell ls ./*.o)")
        otp = self.opciones.split(" ")
        for i in filter(lambda file :file.endswith(".cpp"), self.fuentes.split(" ")):
            self.__compile(i,otp)
        self.__link(self.tipo)
        with open("makefile","w") as make:
            make.writelines([i+"\n" for i in self.__output ])


data = {}
with open(f"{sys.argv[1]}","r") as conf:
    data = json.loads(conf.read())

a = Make(data)

a.make_make()




    

