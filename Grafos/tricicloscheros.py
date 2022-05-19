from pyspark import SparkContext
import sys

#Función que devuelve las aristas como una tupla ordenada
def aristas_ordenadas(lista):
    l=lista.strip().split(',')
    n1=l[0]
    n2=l[1]
    if n1<n2:
         return (n1,n2)
    elif n1>n2:
         return (n2,n1)
    else:
        pass

#Función que devuelve si las aristas existen y si dependen de otro nodo    
def lista_aristas_dep(tupla):
    aristas=[]
    for i in range(len(tupla[1])):
        aristas.append(((tupla[0],tupla[1][i]),'exists'))
        for j in range(i+1,len(tupla[1])):
            if tupla[1][i]<tupla[1][j]:
                aristas.append(((tupla[1][i],tupla[1][j]),('pending',tupla[0])))
            else:
                aristas.append(((tupla[1][j],tupla[1][i]),('pending',tupla[0])))
    return aristas

#Función que filtra para quedarte con los triciclos
def filtro(tupla):
    return (len(tupla[1])>=2 and 'exists' in tupla[1])

#Función que saca los triciclos y los devuelve en forma de tupla
def triciclos(h):
    l=[]
    for i in h[1]:
        if i!='exists':
            l.append((i[1],h[0][0],h[0][1]))
    return l

#Función principal, se sirve de todas las anteriores
def principal(sc,files):
    rdd=sc.parallelize([])
    for file_name in files:    
        file_rdd=sc.textFile(file_name)
        rdd=rdd.union(file_rdd)
    fin=rdd.map(aristas_ordenadas).filter(lambda x: x is not None).distinct()
    adj=fin.groupByKey().mapValues(list).flatMap(lista_aristas_dep).\
        groupByKey().mapValues(list).filter(filtro).flatMap(triciclos)
    print(adj.collect())


if __name__=="__main__":
    if len(sys.argv)<2:
        print("Uso: python3 {0} <file>".format(sys.argv[0]))
    else:
        l=[]
        for i in range(1,len(sys.argv)):
            l.append(sys.argv[i])
        with SparkContext() as sc:
            principal(sc,l)
