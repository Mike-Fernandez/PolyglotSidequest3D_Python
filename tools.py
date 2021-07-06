from enum import Enum
from math_tools import vectorZeroes, zeroes
import classes

def INT_FLOAT(file, item_list, i):
    e0 = 0
    r0 = 0.0
    array  = [float(x) for x in file.readline().split()]
    e0 = int(array[0])
    r0 = array[1]
    item_list[i].setValues(classes.indicators["NOTHING"], classes.indicators["NOTHING"], classes.indicators["NOTHING"], 
        classes.indicators["NOTHING"], e0, classes.indicators["NOTHING"], classes.indicators["NOTHING"], classes.indicators["NOTHING"], 
        classes.indicators["NOTHING"], classes.indicators["NOTHING"], classes.indicators["NOTHING"], classes.indicators["NOTHING"], 
        classes.indicators["NOTHING"], classes.indicators["NOTHING"], r0)

def INT_FLOAT_FLOAT_FLOAT(file, item_list: classes.item, i):
    e = 0
    r = 0.0 
    rr = 0.0 
    rrr = 0.0
    array = [float(x) for x in file.readline().split()]
    e = int(array[0])
    r = array[1]
    rr = array[2]
    rrr = array[3]
    item_list[i].setValues(e, r, rr, rrr, 
        classes.indicators["NOTHING"], classes.indicators["NOTHING"], classes.indicators["NOTHING"], classes.indicators["NOTHING"], 
        classes.indicators["NOTHING"], classes.indicators["NOTHING"], classes.indicators["NOTHING"], classes.indicators["NOTHING"], 
        classes.indicators["NOTHING"], classes.indicators["NOTHING"], classes.indicators["NOTHING"])

def INT10(file, item_list, i):
    e1 = 0
    e2 = 0
    e3 = 0
    e4 = 0
    e5 = 0
    e6 = 0
    e7 = 0
    e8 = 0
    e9 = 0
    e10 = 0
    e11 = 0
    array = [int(x) for x in file.readline().split()]
    e1 = array[0]
    e2 = array[1]
    e3 = array[2]
    e4 = array[3]
    e5 = array[4]
    e6 = array[5]
    e7 = array[6]
    e8 = array[7]
    e9 = array[8]
    e10 = array[9]
    e11 = array[10]
    item_list[i].setValues(e1, classes.indicators["NOTHING"], classes.indicators["NOTHING"], classes.indicators["NOTHING"], 
        e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, classes.indicators["NOTHING"])

switch = {
    classes.modes["INT_FLOAT"]: INT_FLOAT,
    classes.modes["INT_FLOAT_FLOAT_FLOAT"]: INT_FLOAT_FLOAT_FLOAT,
    classes.modes["INT10"]: INT10
}


def obtenerDatos(file, nlines, n, mode, item_list):
    line = ""
#    file = open("3dtest.dat", "r")
    line = file.readline()
    if(nlines == classes.lines["DOUBLELINE"]):
        line = file.readline()
    for i in range(n):
        switch[mode](file, item_list, i)
#        print("Printing itemList from obtenerDatos "+ str(item_list[i].getX()) + " " + str(item_list[i].getY()) + " " + str(item_list[i].getZ()))

def correctConditions(n, list, indices, nNodes, nDirichx, nDirichy, nDirichz):
    #Python deja las variables delclaradas dentro de un grupo de instrucciones accesibles desde fuera, lo que causa problemas si se quiere
    #reusar el mismo nombre de variable
    for r in range(n):
        indices[r] = list[r].getNode1()

    print("Length of dirichlet list" + str(len(list)))

    for m in range(nDirichy):
        list[nDirichx + m].setNode1(list[m].getNode1() + nNodes)
    
    for t in range(nDirichz):
        list[nDirichx + nDirichy + t].setNode1(list[t].getNode1() + 2*nNodes)

    print("DIRICHLET FROM CORRECT CONDITIONS " + str(n))
    for f in range(n):
        print(str(list[f].getNode1())+" "+str(list[f].getValue()))

    for i in range(n-1):
        pivot = list[i].getNode1()
        for j in range(i, n):
            pos = list[j].getNode1()
            if(pos > pivot):
                list[j].setNode1(pos-1)

def addExtension(filename, extension):
    tupla = (filename, extension)
    newFileName = "".join(tupla)
    return newFileName

def leerMallayCondiciones(m, filename):
    inputFileName = ""
    nNodes = 0  
    nEltos=0 
    nDirich=0 
    nNeu = 0
    inputFileName = addExtension(filename, ".dat")
    file = open(inputFileName, "r")
    line  = [float(x) for x in file.readline().split()]
    Ei = line[0]
    f_x = line[1]
    f_y = line[2]
    f_z = line[3]
    line = [int(x) for x in file.readline().split()]
    nNodes = line[0]
    nEltos = line[1]
    nDirichx = line[2]
    nDirichy = line[3]
    nDirichz = line[4]
    nDirich = nDirichx + nDirichy + nDirichz
    nNeu = line[5]

    file.readline()

    m.setParameters(Ei, f_x, f_y, f_z)
    m.setSizes(nNodes, nEltos, nDirich, nNeu)
    m.createData()

    obtenerDatos(file, classes.lines["SINGLELINE"], nNodes, classes.modes["INT_FLOAT_FLOAT_FLOAT"], m.getNodes())
    file.readline()
#    item_list = m.node_list
#    for i in range(10):
#        print("Printing itemList from leerMalla "+ str(item_list[i].getX()) + " " + str(item_list[i].getY()) + " " + str(item_list[i].getZ()))
    obtenerDatos(file, classes.lines["DOUBLELINE"], nEltos, classes.modes["INT10"], m.getElements())
    file.readline()
    obtenerDatos(file, classes.lines["DOUBLELINE"], nDirichx+nDirichy+nDirichz, classes.modes["INT_FLOAT"], m.getDirichlet())
#    temp = file.readline()
#    print("line after reading dirichletX"+temp)
#    obtenerDatos(file, classes.lines["DOUBLELINE"], nDirichy, classes.modes["INT_FLOAT"], m.getDirichlet())
#    temp = file.readline()
#    print("line after reading dirichletY"+temp)
#    obtenerDatos(file, classes.lines["DOUBLELINE"], nDirichz, classes.modes["INT_FLOAT"], m.getDirichlet())
    temp = file.readline()
    print("line after reading dirichletZ"+temp)
    obtenerDatos(file, classes.lines["DOUBLELINE"], nNeu, classes.modes["INT_FLOAT"], m.getNeumann())

    file.close()
    correctConditions(nDirich, m.getDirichlet(), m.getDirichletIndices(), m.getSize(classes.sizes["NODES"]), nDirichx,nDirichy, nDirichz)
    print("After correcting the conditions")

def findIndex(v, s, arr):
    for i in range(s):
        if(arr[i] == v):
            return True
    return False

def writeResults(m, T, filename):
    outputFilename = ""
    dirichIndices = m.getDirichletIndices()
    dirich = m.getDirichlet()

    outputFilename = addExtension( filename, ".post.res")
    print(outputFilename)
    file = open(outputFilename, "w")

    file.write("GiD Post Results File 1.0\n")
    file.write("Result \"Temperature\" \"Load Case 1\" 1 Scalar OnNodes\nComponentNames \"T\"\nValues\n")

    Tpos = 0
    Dpos = 0
    n = m.getSize(classes.sizes["NODES"])
    nd = m.getSize(classes.sizes["DIRICHLET"])
    for i in range(n):
        if(findIndex(i+1, nd, dirichIndices)):
            string = str(i+1) + " " + str(dirich[Dpos].getValue()) + "\n"
            file.write(string)
            Dpos+= 1
        else:
            string2 = str(i+1) + " " + str(T[Tpos]) + "\n"
            file.write(string2)
            Tpos+= 1
    
    file.write("End values\n")
    file.close()

#m = classes.mesh()
#leerMallayCondiciones(m, "ProyectoPolyglot")

#m.node_list[0].setX(9)
#print(m.node_list[0].getX())
#print(m.getNode(0).getX())

#print("NODES")
#for i in range(m.getSize(classes.sizes["NODES"])):
#    print(str(m.getNodes()[i].getX())+" "+str(m.getNodes()[i].getY())+" "+str(m.getNodes()[i].getZ()))
#print("ELEMENTS")
#for i in range(m.getSize(classes.sizes["ELEMENTS"])):
#    print(str(m.getElements()[i].getNode1())+" "+str(m.getElements()[i].getNode2())+" "+str(m.getElements()[i].getNode3())+" "+str(m.getElements()[i].getNode4())
#        +" "+str(m.getElements()[i].getNode5()) +" "+str(m.getElements()[i].getNode6()) +" "+str(m.getElements()[i].getNode7()) +" "+str(m.getElements()[i].getNode8())
#        +" "+str(m.getElements()[i].getNode9()) +" "+str(m.getElements()[i].getNode10()))
#print("NEUMANN")
#for i in range(m.getSize(classes.sizes["NEUMANN"])):
#    print(str(m.getNeumann()[i].getNode1())+" "+str(m.getNeumann()[i].getValue()))
#dirich_indices = m.getDirichletIndices()
#print("DIRICHLET INDICES")
#for i in range(m.getSize(classes.sizes["DIRICHLET"])):
#    print(str(m.getDirichletIndices()[i]))
#print("DIRICHLET")
#for i in range(m.getSize(classes.sizes["DIRICHLET"])):
#    print(str(m.getDirichlet()[i].getNode1())+" "+str(m.getDirichlet()[i].getValue()))
#m.getDirichlet()[0].setNode1(4)
#print("DIRICHLET")
#for i in range(m.getSize(classes.sizes["DIRICHLET"])):
#    print(str(m.getDirichlet()[i].getNode1())+" "+str(m.getDirichlet()[i].getValue()))

#obtenerDatos("3dtest.dat", 0, 0, 0, 0)
#T = []
#vectorZeroes(T,30)
#writeResults(m,T,"ProyectoPolyglot")