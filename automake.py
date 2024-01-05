import json
import sys
import os

output = []

if (len(sys.argv[1])>=2):
    with open(sys.argv[1],"r") as data:
        nolose = json.loads(data.read())
    output.append("objects = $(shell ls ./*.o)\n")

    include = nolose["directorio_de_cabeceras"]
    include_parsed  = ""
    
    for i in include.split(" "):
        i = "-I"+i
        include_parsed += i
        include_parsed +=" "
    output.append(f"Include = {include_parsed}\n")
    libs = nolose["librerias"]
    libs_parsed  = ""
    
    for i in libs.split(" "):
        i = "-l"+i
        libs_parsed += i
        libs_parsed +=" "
    output.append(f"lib = {libs_parsed}\n")

    all_rule_dependecies=""
    for i in os.listdir(nolose["fuentes"]):
        output.append(f"{i.split('.')[0]}.o:{nolose['fuentes']}/{i}\n")
        output.append(f"\t{nolose['compilador']} -c {nolose['fuentes']}/{i} $(Include)\n")
        all_rule_dependecies += f"{i.split('.')[0]}.o "

    output.append(f"all:{all_rule_dependecies}\n")
    output.append(f"\t{nolose['compilador']} -o {nolose['directorio_del_ejecutable']}/{nolose['nombre']} $(objects) $(lib)\n")

    with open("makefile","w") as target:
        for i in output:
            target.write(i)
