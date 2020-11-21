#!/usr/bin/python
# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import pcontas_geracao

# pyinstaller --icon=alter.ico --onefile --noconsole pcontas_fortes.py

# update wcont.hist set dshistoricopadrao=REPLACE(dshistoricopadrao, '???', '' ) 

# LightGreen3, Topanga
# sg.theme('Dark Blue 3')

def new_lay():
    # Carregamento da tela.
    layout = [
            [sg.Text('****** ORIENTAÇÕES ******', font=('Arial', 10, 'bold'), size=(100, 1) , justification='center')],
            [sg.Text('**************************************************************************************************************************************', font=('Arial', 10, 'bold'), size=(100, 1) , justification='left')],
            [sg.Text('1 - Abra o Fortes Contábil.')],
            [sg.Text('2 - Abra o cadastro de planos de contas, liste as contas.')],
            [sg.Text('3 - Clique em "IMPRIMIR".')],
            [sg.Text('4 - Deixe as colunas da forma que estão (Classificação, Descrição, Reduzido, Natureza, Sintética).')],
            [sg.Text('5 - Clique em "EXPORTAR CSV".')],
            [sg.Text('6 - Selecione este mesmo arquivo abaixo:')],
            [sg.Text('7 - Após gerar confira se o delimitador é um ";" ponto e vírgula!')],

            [sg.Text(' ', font=('Arial', 10, 'bold'), size=(70, 1) , justification='center')],

            [sg.Text('DEFINA ABAIXO AS COLUNAS NO SEU CSV PARA O PLANO DE CONTAS', font=('Arial', 10, 'bold'), size=(100, 1) , justification='center')],
            [sg.Text('**************************************************************************************************************************************', font=('Arial', 10, 'bold'), size=(100, 1) , justification='left')],


            [sg.Text('Classificação', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'), 
            sg.Text('Descrição', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'), 
            sg.Text('Reduzido', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'),         
            sg.Text('Dev/Cred', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'), 
            sg.Text('Sintética', font=('Arial', 10, 'bold'), size=(14, 1), justification='center')],

            [sg.Text('A', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'), 
            sg.Text('B', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'), 
            sg.Text('C', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'),         
            sg.Text('D', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'),
            sg.Text('E', font=('Arial', 10, 'bold'), size=(14, 1), justification='center')],

            [sg.Text(' ', font=('Arial', 10, 'bold'), size=(70, 1) , justification='center')],
            
            [sg.Text('DEFINA ABAIXO AS COLUNAS NO SEU CSV PARA O MOVIMENTO', font=('Arial', 10, 'bold'), size=(100, 1) , justification='center')],
            [sg.Text('**************************************************************************************************************************************', font=('Arial', 10, 'bold'), size=(100, 1) , justification='left')],
            [sg.Text('Devedora', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'), 
            sg.Text('Credora', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'), 
            sg.Text('Data', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'),         
            sg.Text('Valor', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'), 
            sg.Text('Histórico', font=('Arial', 10, 'bold'), size=(14, 1), justification='center')],

            [sg.Text('A', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'), 
            sg.Text('B', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'), 
            sg.Text('C', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'),         
            sg.Text('D', font=('Arial', 10, 'bold'), size=(14, 1), justification='center'), 
            sg.Text('E', font=('Arial', 10, 'bold'), size=(14, 1), justification='center')],            

            [sg.Text(' ', font=('Arial', 10, 'bold'), size=(70, 1) , justification='center')],

            [sg.Text('P. Contas:', font=('Arial', 10, 'bold'), size=(13, 1)), 
             sg.Input(size=(70, 1)), 
             sg.FileBrowse(file_types=(("Text Files", "*.csv"),), tooltip='Procure seu arquivo clicando aqui.', button_text='Localizar')],

            [sg.Text('Movimentação:', font=('Arial', 10, 'bold'), size=(13, 1)), 
             sg.Input(size=(70, 1)), 
             sg.FileBrowse(file_types=(("Text Files", "*.csv"),), tooltip='Procure seu arquivo clicando aqui.', button_text='Localizar')],

            [sg.Submit(tooltip='Clique para converter.', button_text='Converter'), sg.Cancel(tooltip='Clique para cancelar.', button_text='Cancelar')]]

    return layout

# Barra de títuloda aplicação.
window = sg.Window('Converte plano de contas CSV para Alterdata.', new_lay(), icon=r'C:\Users\ALTERDATA\Desktop\alter.ico').Finalize()

event, values = window.read()





#class Exportar(file_plano, file_movimento):
#	def save(self, code):
#		print(code.text)
#		with open('test.py', 'w') as f:
#			# Conteúdo do arquivo
#			f.write(code.text)
#			
#	def load(self, code):
#		with open('test.py', 'r') as f:
#			# Conteúdo do arquivo
#			code.text = f.read()

#def verifica_diretorio(caminho, campo):
#    try:
#        return open(caminho, encoding='latin-1')
#    except:
#        print('Teu cú em ', campo)
#
#
#verifica_diretorio(values[1], 'Movimentações')
#
#exporta_plano(verifica_diretorio(values[0], 'Plano de Contas'))



# Verifica se o campo possui o caminho do arquivo de plano de contas a ser convertido.
if values[0]:
    pcontas_geracao.cria_pasta()
    
    file_plano = open(values[0], encoding='latin-1')

    pcontas_geracao.exporta_plano(file_plano)
    pcontas_geracao.diretorios(values[0])
else:
    sg.popup("Atenção", "Para converter o plano de contas \né preciso selecionar o arquivo!")

# Verifica se o campo possui o caminho do arquivo de movimento a ser convertido.
if values[1]:
    if values[0]:   
        file_movimento = open(values[1], encoding='latin-1')
        pcontas_geracao.exporta_movimento(file_movimento)
    else:
        sg.popup("Atenção", "Para converter a movimentação \né preciso selecionar o plano de contas!")

window.close()

#select * from wcont.pcont
#select * from wcont.contas where idplanodecontas=3
#update wcont.contas set tpconta='A' where length(cdclassinterna)>=11
#update wcont.contas set idorigem='D' where substring(cdclassinterna,1, 1)='1'
