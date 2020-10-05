import csv
import PySimpleGUI as sg

# pyinstaller --icon=alter.ico --onefile --noconsole pcontas_fortes.py
# update wcont.hist set dshistoricopadrao=REPLACE(dshistoricopadrao, '???', '' ) 

# LightGreen3, Topanga
# sg.theme('Dark Blue 3')

'''
            [sg.InputText('A', size=(12, 1), justification='center'), 
             sg.InputText('B', size=(12, 1), justification='center'), 
             sg.InputText('C', size=(12, 1), justification='center'), 
             sg.InputText('D', size=(12, 1), justification='center'), 
             sg.InputText('E', size=(12, 1), justification='center')],
'''
def new_lay():
    # Carregamento da tela.
    layout = [
            [sg.Text('****** ORIENTAÇÕES ******', font=('Arial', 10, 'bold'), size=(70, 1) , justification='center')],
            [sg.Text('****************************************************************************************************************', font=('Arial', 10, 'bold'), size=(70, 1) , justification='center')],
            [sg.Text('1 - Abra o Fortes Contábil.')],
            [sg.Text('2 - Abra o cadastro de planos de contas, liste as contas.')],
            [sg.Text('3 - Clique em "IMPRIMIR".')],
            [sg.Text('4 - Deixe as colunas da forma que estão (Código, Descrição, Reduzido, Natureza).')],
            [sg.Text('5 - Clique em "EXPORTAR CSV".')],
            [sg.Text('6 - Selecione este mesmo arquivo abaixo:".')],

            [sg.Text(' ', font=('Arial', 10, 'bold'), size=(70, 1) , justification='center')],

            [sg.Text('****** DEFINA ABAIXO AS COLUNAS NO SEU CSV PARA O PLANO DE CONTAS******', font=('Arial', 10, 'bold'), size=(70, 1) , justification='center')],
            [sg.Text('****************************************************************************************************************', font=('Arial', 10, 'bold'), size=(70, 1) , justification='center')],


            [sg.Text('Código', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'), 
            sg.Text('Descrição', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'), 
            sg.Text('Reduzido', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'),         
            sg.Text('Natureza', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'), 
            sg.Text('Histórico', font=('Arial', 10, 'bold'), size=(10, 1), justification='center')],

            [sg.Text('A', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'), 
            sg.Text('B', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'), 
            sg.Text('C', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'),         
            sg.Text('D', font=('Arial', 10, 'bold'), size=(10, 1), justification='center')],

            [sg.Text(' ', font=('Arial', 10, 'bold'), size=(70, 1) , justification='center')],
            
            [sg.Text('****** DEFINA ABAIXO AS COLUNAS NO SEU CSV PARA O MOVIMENTO******', font=('Arial', 10, 'bold'), size=(70, 1) , justification='center')],
            [sg.Text('****************************************************************************************************************', font=('Arial', 10, 'bold'), size=(70, 1) , justification='center')],
            [sg.Text('Devedora', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'), 
            sg.Text('Credora', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'), 
            sg.Text('Data', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'),         
            sg.Text('Valor', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'), 
            sg.Text('Histórico', font=('Arial', 10, 'bold'), size=(10, 1), justification='center')],

            [sg.Text('A', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'), 
            sg.Text('B', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'), 
            sg.Text('C', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'),         
            sg.Text('D', font=('Arial', 10, 'bold'), size=(10, 1), justification='center'), 
            sg.Text('E', font=('Arial', 10, 'bold'), size=(10, 1), justification='center')],            

            [sg.Text(' ', font=('Arial', 10, 'bold'), size=(70, 1) , justification='center')],

            [sg.Text('P. Contas:', font=('Arial', 10, 'bold'), size=(13, 1)), 
             sg.Input(), 
             sg.FileBrowse(file_types=(("Text Files", "*.csv"),), tooltip='Procure seu arquivo clicando aqui.', button_text='Localizar')],

            [sg.Text('Movimentação:', font=('Arial', 10, 'bold'), size=(13, 1)), 
             sg.Input(), 
             sg.FileBrowse(file_types=(("Text Files", "*.csv"),), tooltip='Procure seu arquivo clicando aqui.', button_text='Localizar')],

            [sg.Submit(tooltip='Clique para converter.', button_text='Converter'), sg.Cancel(tooltip='Clique para cancelar.', button_text='Cancelar')]]

    return layout

# Barra de títuloda aplicação.
window = sg.Window('Converte plano de contas Fortes para Alterdata.', new_lay(), icon=r'C:\Users\ALTERDATA\Desktop\alter.ico').Finalize()

event, values = window.read()


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

# Cria dicionário para verificar a conversão dos movimentos.
de_para = {}


# Cria o arquivo TXT para montar o plano decontas convertido.
plano_de_contas = open('PlanoDeContasConvertido.txt', 'w')

existentes = []

def lista_reduzidas(file_plano):
    reader_lista = csv.reader(file_plano, delimiter=";")
    for col in reader_lista:
        if col[2] != '':
            existentes.append(col[2])
            print(col[2])

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


# Função para exportar o plano decontas convertido.
def exporta_plano(file_plano):
    reader = csv.reader(file_plano, delimiter=";")
    lista_reduzidas(file_plano)

    i = 0
    file_plano.seek(0)
    for row in reader:
        if row[2] == '':
            i += 1
            while procura_repetidas(str(i)):
                i += 1
                #print(i-1, ' existe lá! Novo i', i)
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
              
        plano_de_contas.write(raiz.ljust(30) + 
                      ''.ljust(30) + 
                      str(reduzida).ljust(10) + 
                      tipo_conta(row[3]).ljust(1) + 
                      cap_name(row[1][:50]).ljust(50) + 
                      origem_conta(row[3]).ljust(1) + 
                      'I'.ljust(1) + 
                      'N'.ljust(1) + 
                      'N'.ljust(1) + 
                      ' '.ljust(15) + 
                      ' '.ljust(15) + 
                      '0' * (10) + 
                      'N'.ljust(1) + 
                      ' '.ljust(10) + 
                      '0' * (10) + 
                      'N'.ljust(1) +
                      'N'.ljust(1) +
                      'N'.ljust(1) +
                      ' '.ljust(50) +
                      ' '.ljust(15) +
                      'N'.ljust(1) +
                      'N'.ljust(1) +
                      '0' * (10) + 
                      ' ' * (30) + 
                      '0' * (10) + 
                      ' ' * (12) + 
                      ' ' * (10) + 
                      ' ' * (30) + 
                      ' ' * (30) + 
                      ' ' * (20) + 
                      "\n")               

    plano_de_contas.close()

    #for k, v in de_para.items():
    #    print(k, ':', v)
    sg.popup("Plano de Contas", "O plano de contas foi convertido!")

def conversor_de_chamada(classificacao):
    for k, v in de_para.items():
        if k == classificacao: 
            print('Se ', k, '==', classificacao, 'retorne ', v)
            return v
            break


# Cria o arquivo TXT para montar o plano decontas convertido.
movimento_fortes = open('MovimentoFortesConvertido.txt', 'w')

def exporta_movimento(file_movimento):
    reader = csv.reader(file_movimento, delimiter=";")

    for row in reader:
        if (row[0] == '(diversas)') | (row[1] == '(diversas)'):
            next(reader)
        else:
            deb = conversor_de_chamada(row[0])
            cred = conversor_de_chamada(row[1])   

            movimento_fortes.write('"' + '"' + ',' +
                          '"' + deb + '"' + ',' +
                          '"' + cred + '"' + ',' +
                          '"' + row[2] + '"' + ',' +
                          '"' + row[3] + '"' + ',' +
                          '"' + '"' + ',' +
                          '"' + row[4] + '"' + ',' +
                          '"' + '"' + ',' +
                          "\n")            
    movimento_fortes.close()
    sg.popup("Movimento contábil", "O movimento foi convertido!")


# Verifica se o campo possui o caminho do arquivo de plano de contas a ser convertido.
if values[5]:
    file_plano = open(values[5], encoding='latin-1')

    exporta_plano(file_plano)
else:
    sg.popup("Atenção", "Para converter o plano de contas \né preciso selecionar o arquivo!")

# Verifica se o campo possui o caminho do arquivo de movimento a ser convertido.
if values[6]:
    if values[5]:   
        file_movimento = open(values[6], encoding='latin-1')
        exporta_movimento(file_movimento)
    else:
        sg.popup("Atenção", "Para converter a movimentação \né preciso selecionar o plano de contas!")

window.close()
