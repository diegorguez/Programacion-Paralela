
from random import randint
from multiprocessing import Process, Array
from multiprocessing import BoundedSemaphore, Semaphore

    

NPROD=randint(1,20)
NCONS=randint(1,10)
N=randint(1,10)

def minimo(lista):
    n=len(lista)
    l=[0]*n
    ma=max(lista)
    for i in range(n):
        if lista[i]!=-1:
            l[i]=lista[i]
        else:
            l[i]=ma+1  
    mi=l[0]
    indice=0
    for i in range(1,len(l)):
        if l[i]<mi and l[i]!=-1:
            mi=l[i]
            indice=i     
    return mi,indice

    
def producer(lista,buffer,indice):
     v=0
     for k in range(N):
         v+=randint(0,10)
         lista[2*indice].acquire()
         buffer[indice]=v
         lista[2*indice+1].release() 
     v=-1
     lista[2*indice].acquire() 
     buffer[indice]=v
     lista[2*indice+1].release() 
     

def listas2(lista, buffer):  
    l=[]
    for i in range(NPROD):
        lista[2*i+1].acquire()
    while [-1]*NPROD!=list(buffer):
        v, indice=minimo(buffer)
        l.append(v)
        lista[2*indice].release()
        lista[2*indice+1].acquire() 
    print("Resultado =",l)
    
    
def main():
     buffer=Array('i',NPROD)
     semaf=[]
     for i in range(NPROD):
         semaf.append(BoundedSemaphore(1))
         semaf.append(Semaphore(0))
     l=[]
     for index in range(NPROD):
         l.append(Process(target=producer,args=(semaf, buffer, index)))
     l.append(Process(target=listas2,args=(semaf, buffer)))
     for p in l:
         p.start()
     for p in l:
         p.join()


if __name__ == "__main__":
 main()    
           
        
        
"""def produce():
    l=[]
    n=randint(2,20)
    for i in range(0,n-1):
        if i==0:
            l.append(randint(0,100))
        else:
            l.append(randint(l[i-1],l[i-1]+10000))
    l.append(-1)
    print(l)

NPROD=randint(1,20)
def main():
    l=[]
    for i in range(0,NPROD):
        l.append(Process(target=produce(),))
    for p in l:
        p.start()
    for p in l:
        p.join()

if __name__=="__main__":
    main()"""
