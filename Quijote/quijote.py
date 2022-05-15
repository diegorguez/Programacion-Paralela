import os
import random as rd

def extract_random_lines(entrada,salida):
    #función para obtener un número "aleatorio" de líneas.
    porcentaje=rd.randint(1,100)
    fentrada=open(entrada,"r")
    fsalida=open(salida,"w")
    ffilas=fentrada.readlines()
    for linea in ffilas:
        dado=rd.randint(1,100)
        if dado<porcentaje:
            fsalida.write(linea)
    fentrada.close()
    fsalida.close()

def count_words_quijote(entrada,salida):
    #función que cuenta las palabras del fichero, creando un fichero copia que afirme el número de palabras.
    fentrada=open(entrada,"r")
    fsalida=open(salida,"w")
    ffilas=fentrada.readlines()
    acumulador=0
    for linea in ffilas:
        listapalabras=linea.split()
        acumulador+=len(listapalabras)
    fsalida.write(f"{acumulador}")
    fentrada.close()
    fsalida.close()

#ejecutamos lo que se nos pide
extract_random_lines("Quijote","quijote_s05")   
count_words_quijote("quijote_s05","out_quijote_s05")
count_words_quijote("Quijote","out_quijote")
