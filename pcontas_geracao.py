#!/usr/bin/python
# -*- coding: utf-8 -*-

import PySimpleGUI as sg

import os
import os.path
import shutil

import csv

from xml.etree.ElementTree import Element, ElementTree, tostring
import xml.etree.ElementTree as etree


#class Geracao:
#    def __init__(self):
#        # Cria dicionário para verificar a conversão dos movimentos.
#        self.de_para = {}
#        # Cria lista para função lista_reduzidas.
#        self.existentes = []        

# Cria dicionário para verificar a conversão dos movimentos.
de_para = {}
# Cria lista para função lista_reduzidas.
existentes = [] 
 

# Verifica sea conta é analítica ou sintética.
def tipo_conta(tipo):
    if tipo == 'X':
        return 'A'
    else:
        return 'S'


# verifica se a conta temorigem Credora ou Devedora.
def origem_conta(origem):
    if origem == 'Devedora':
        return 'D'
    elif origem == 'Credora':
        return 'C'
    else:
        return 'I'    

def cria_arquivo_plano():
    # Cria o arquivo TXT para montar o plano decontas convertido dentro da pasta CONVERTIDOS.
    plano_de_contas = open(os.path.join(os.getcwd(), 'CONVERTIDOS', 'PlanoDeContasConvertido.txt'), 'w')
    return plano_de_contas

#plano_de_contas = open(os.path.join(os.getcwd(), 'CONVERTIDOS', 'PlanoDeContasConvertido.txt'), 'w')

def cria_arquivo_movimento():
    # Cria o arquivo TXT para montar o plano decontas convertido dentro da pasta CONVERTIDOS.
    movimento_fortes = open(os.path.join(os.getcwd(), 'CONVERTIDOS', 'MovimentoFortesConvertido.txt'), 'w')        
    return movimento_fortes


# VERIFICAR SE É , OU ; ANTES DE TUDO
def lista_reduzidas(file_plano):
    reader_lista = csv.reader(file_plano, delimiter=";")
    for col in reader_lista:
        if col[2] != '':
            existentes.append(col[2])
            #print(col[2])


def procura_repetidas(search):
    if search in existentes:
        return True


def cap_name(name):
    p = ['da','das', 'de', 'di', 'do','dos', 'du', 'para', 'com', 'a', 'e', 'S/A']
    items = []
    for item in name.split():
        if not item.lower() in p:
            item = item.capitalize()
        else:
            item = item.lower()
        items.append(item)
    return ' '.join(items)


def verifica_estilo_classificacao(raiz):
    if len(raiz)>1 and raiz[1] != '.':
        return raiz[0]+'.'+raiz[1:]
    else:
        return raiz


# Função para exportar o plano decontas convertido.
def exporta_plano(file_plano):
    plano_de_contas = cria_arquivo_plano()

    reader = csv.reader(file_plano, delimiter=";")
    
    lista_reduzidas(file_plano)
    
    i = 0
    file_plano.seek(0)
    for row in reader:
        if row[2] == '':
            i += 1
            while procura_repetidas(str(i)):
                i += 1
            else:
                reduzida = str(i)                
        else:
            reduzida = str(row[2])  
        if '-' in row[0]:
            raiz, dv = row[0].split('-')
            
        else:
            raiz = row[0]
            
        # Adiciona indices para localizar no dicionário.
        de_para.update({str(raiz):str(reduzida)})
            
        plano_de_contas.write(verifica_estilo_classificacao(raiz).ljust(30) + 
                    ''.ljust(30) + 
                    str(reduzida).ljust(10) + 
                    tipo_conta(row[3]).ljust(1) + 
                    cap_name(row[1][:50]).ljust(50) + 
                    origem_conta(row[4]).ljust(1) + 
                    'I'.ljust(1) + 
                    'N'.ljust(1) + 
                    'N'.ljust(1) + 
                    ' '.ljust(15) + 
                    ' '.ljust(15) + 
                    '0' * (10) + 
                    'N'.ljust(1) + 
                    ' '.ljust(10) + 
                    '0' * (7) + 
                    ',00' + 
                    'N'.ljust(1) +
                    'N'.ljust(1) +
                    ' '.ljust(51) +
                    ' '.ljust(15) +
                    'N'.ljust(1) +
                    'N'.ljust(1) +
                    '0' * (10) + 
                    ' ' * (30) + 
                    '0' * (11) + 
                    ' ' * (11) + 
                    '0' + 
                    ' ' * (9) + 
                    ' ' * (30) + 
                    ' ' * (30) + 
                    ' ' * (20) + 
                    "\n")               
    plano_de_contas.close()

    for c, v in de_para.items():
        print(c, v)

    sg.popup("Plano de Contas", "O plano de contas foi convertido!")


def conversor_de_chamada(classificacao):
    for k, v in de_para.items():
        if k == classificacao: 
            #print('Se ', k, '==', classificacao, 'retorne ', v)
            #print(v)
            return v
            break


#print(os.path.join(os.getcwd(), 'CONVERTIDOS', 'MovimentoFortesConvertido.txt'))
def exporta_movimento(file_movimento):
    movimento_fortes = cria_arquivo_movimento()
    
    reader = csv.reader(file_movimento, delimiter=";")
    for row in reader:
        if (row[0] == '(diversas)') | (row[1] == '(diversas)'):
            try:
                next(reader)
            except StopIteration:
                pass    
        else:
            deb = conversor_de_chamada(row[0])
            cred = conversor_de_chamada(row[1])   
            movimento_fortes.write('"' + '"' + ',' +
                        '"' + deb + '"' + ',' +
                        '"' + cred + '"' + ',' +
                        '"' + row[2] + '"' + ',' +
                        '"' + row[3].replace('.', '') + '"' + ',' +
                        '"' + '"' + ',' +
                        '"' + row[4] + '"' + ',' +
                        '"' + '"' + ',' +
                        "\n")            
    movimento_fortes.close()
    sg.popup("Movimento contábil", "O movimento foi convertido!")


def diretorios(file_plano):
    diretorio = file_plano
    arquivo_dir = open('dir.xml', 'wb')
    root = Element('diretorios')
    tree = ElementTree(root)
    plano = Element('plano')
    root.append(plano)
    plano.text = file_plano
    root.set('id', '1')
    print(diretorio)
    #print(etree.tostring(root))
    tree.write(arquivo_dir)
    arquivo_dir.close()


# Crio um diretório para salvar as movimentações. 
def cria_pasta():
    if not os.path.exists('CONVERTIDOS'):
        os.mkdir('CONVERTIDOS')    
