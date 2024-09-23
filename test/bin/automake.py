import json
import sys
import os
import platform

class Make:
    def __init__(self , data):
        self.compilador:str =                data["compilador"]
        self.fuentes:str =                   data["fuentes"]
        self.directorio_de_cabeceras:str =   data["directorio_de_cabeceras"]
        try:   
            self.librerias:str =                 data["librerias"]
        except KeyError:
            self.librerias = None
        self.directorio_de_ejecutable:str =  data["directorio_del_ejecutable"]
        self.nombre:str =                    data["nombre"]
        self.tipo:str =                      data["tipo"]
        self.opciones:str =                  data["opciones"]
        try:
            self.directorio_de_librerias =        data["directorio_de_librerias"]
        except KeyError:
            self.directorio_de_librerias = None
        self.__output =                    []
    def __declare_var(self,name,value):
        self.__output.append(name + " = " +value)
    def __declare_rule(self,name,dependecies:list[str],commands):
        self.__output.append(name + ":" + dependecies)
       
        self.__output.append("\t"+commands)
    def __compile(self,file,options):
        obj = file.split("/")[-1]
        obj = obj.replace(".cpp",".o")
        self.__declare_rule(obj,file,f"{self.compilador} -c {file} {options} $(Include)")
    def __link(self,type):
        obj= filter(lambda f: f.endswith(".cpp"),os.listdir(self.fuentes))
        objs = ""
        for i in obj:
            objs += i+" "
        objs=objs.replace(".cpp",".o")
        match type:
            case "shared":
                match platform.system():
                    case "Linux":
                        self.__declare_rule("all",objs,f"{self.compilador} -shared -fPIC -o {self.directorio_de_ejecutable}/lib{self.nombre}.so $(objects) $(lib)")
                    case "Windows":
                        self.__declare_rule("all",objs,f"{self.compilador} -shared -fPIC -o {self.directorio_de_ejecutable}/lib{self.nombre}.dll $(objects) $(lib)")
                    case "Darwin":
                        self.__declare_rule("all",objs,f"{self.compilador} -shared -fPIC -o {self.directorio_de_ejecutable}/lib{self.nombre}.dylib $(objects) $(lib)")
                    case _:
                        raise ValueError("This platform is not suported")
            case "static":
                
               
                self.__declare_rule(
                    "all",
                    objs,
                    f"ar rcs {self.nombre}.a  $(objects)"
                )
            case "app":
                match platform.system():
                    case "Linux":
                        self.__declare_rule("all",objs,f"{self.compilador} -o {self.directorio_de_ejecutable}/{self.nombre} $(objects) $(lib)")
                    case "Windows":
                        self.__declare_rule("all",objs,f"{self.compilador} -o {self.directorio_de_ejecutable}/{self.nombre}.exe $(objects) $(lib)")
                    case "Darwin":
                        self.__declare_rule("all",objs,f"{self.compilador} -o {self.directorio_de_ejecutable}/{self.nombre} $(objects) $(lib)")
                    case _:
                        raise ValueError("This platform is not suported")
            case _:
                raise ValueError("Option not suported")
    def make_make(self):
        inc = ""
        for i in self.directorio_de_cabeceras.split(" "):
            inc += ("-I"+i)+" "
        self.__declare_var("Include",inc)
        if (self.librerias != None):
            lib = ""
            for j in self.librerias.split(" "):
                if j.endswith(".a"):
                    lib += j + " "
                else:
                    lib += "-l"+j+" "
        
            self.__declare_var("lib",lib)
        if (self.directorio_de_librerias != None):
            self.__declare_var("libpath",self.directorio_de_librerias)
        self.__declare_var("objects", "$(shell ls ./*.o)")
        
        for i in filter(lambda file :file.endswith(".cpp"), os.listdir(self.fuentes)):
            self.__compile(self.fuentes+"/"+i,self.opciones)
        self.__link(self.tipo)
        obj= filter(lambda f: f.endswith(".cpp"),os.listdir(self.fuentes))
        objs = ""
        for i in obj:
            objs += "./"+i+" "
        objs=objs.replace(".cpp",".o")
        self.__declare_rule("clear","",f"rm -r $(objects)")
        return self.__output
        


data = {}
with open(f"{sys.argv[1]}","r") as conf:
    data = json.loads(conf.read())
with open(f"makefile","w") as make :
    make.truncate()
if data["incluir"]:
    makes = []
    a = Make(data)
    rawmake = a.make_make()
    makes.append(rawmake)
    for i in data["incluir"].split(" "):
        with open(f"{i}","r") as conf:
            data = json.loads(conf.read())
        sub = Make(data)
        sub2 = sub.make_make()
        makes.append(sub2)
    makes.reverse()
    for i in makes[:-1]:
        for j in i:
            if "clear:" in j:
                
                i.pop(i.index(j)+1)
                i.pop(i.index(j))
            

    for i in makes:
        with open(f"makefile","a") as make:
            make.writelines(j+"\n" for j in i )  

    
else:
    a = Make(data)
    rawmake = a.make_make()
    with open("makefile","w") as make :
        make.writelines(i+ "\n" for i in rawmake)




    

