import csv
import PySimpleGUI as sg

#update wcont.hist set dshistoricopadrao=REPLACE(dshistoricopadrao, '???', '' ) 

sg.theme('Light Blue 2')

# Carregamento da tela.
layout = [
        [sg.Text('****** DEFINA ABAIXO AS COLUNAS NO SEU CSV ******', size=(70, 1) , justification='center')],
        [sg.Text('Data', size=(12, 1), justification='center'), 
        sg.Text('Devedora', size=(12, 1), justification='center'), 
        sg.Text('Credora', size=(12, 1), justification='center'), 
        sg.Text('Valor', size=(12, 1), justification='center'), 
        sg.Text('Histórico', size=(12, 1), justification='center'),    ],

        [sg.InputText('A', size=(12, 1), justification='center'), 
         sg.InputText('D', size=(12, 1), justification='center'), 
         sg.InputText('G', size=(12, 1), justification='center'), 
         sg.InputText('J', size=(12, 1), justification='center'), 
         sg.InputText('E', size=(12, 1), justification='center')],

        [sg.Text('1 - Abra o Fortes Contábil.')],
        [sg.Text('2 - Abra o cadastro de planos de contas, liste as contas.')],
        [sg.Text('3 - Clique em "IMPRIMIR".')],
        [sg.Text('4 - Deixe as colunas da forma que estão (Código, Descrição, Reduzido, Natureza).')],
        [sg.Text('5 - Clique em "EXPORTAR CSV".')],
        [sg.Text('6 - Selecione este mesmo arquivo abaixo:".')],
          
        [sg.Text('Arquivo', size=(8, 1)), sg.Input(), sg.FileBrowse(tooltip='Procure seu arquivo clicando aqui.', button_text='Diretório')],
        [sg.Text('Arquivo', size=(8, 1)), sg.Input(), sg.FileBrowse(tooltip='Procure seu arquivo clicando aqui.', button_text='Diretório')],
          
        [sg.Submit(tooltip='Clique para converter.', button_text='Converter'), sg.Cancel(tooltip='Clique para cancelar.', button_text='Cancelar')]]

# Barra de títuloda aplicação.
window = sg.Window('Converte plano de contas Fortes para Alterdata.', layout)

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

# Função para exportar o plano decontas convertido.
def exporta_plano(file_plano):
    reader = csv.reader(file_plano, delimiter=";")
    i = 0
    for row in reader:
        if row[2] == '':
            i += 1
            reduzida = str(i)
        else:
            reduzida = str(row[2])

        # Adiciona indices para localizar no dicionário.
        # 1.1.2.01.02.01-1
        de_para.update({str(row[0][:14]):str(reduzida)})
              
        plano_de_contas.write(row[0][:14].ljust(30) + 
                      ''.ljust(30) + 
                      str(reduzida).ljust(10) + 
                      tipo_conta(row[3]).ljust(1) + 
                      row[1][:50].ljust(50) + 
                      origem_conta(row[6]).ljust(1) + 
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
    #    print(k[:14], ':', v)

def conversor_de_chamada(classificacao):
    #print('Classificação recebida: ', classificacao)
    for k, v in de_para.items():
        if k == classificacao: 
            #print('Se ', k, '==', classificacao, 'retorne ', v)
            return v
            break
        #return retorno


# Cria o arquivo TXT para montar o plano decontas convertido.
movimento_fortes = open('MovimentoFortesConvertido.txt', 'w')

def exporta_movimento(file_movimento):
    reader = csv.reader(file_movimento, delimiter=";")

    for row in reader:

        deb = conversor_de_chamada(row[0][:14])
        cred = conversor_de_chamada(row[1][:14])   

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


# Verifica se o campo possui o caminho do arquivo de plano de contas a ser convertido.
if values[5]:
    #print('Existe!')
    file_plano = open(values[5], encoding='latin-1')
    exporta_plano(file_plano)

# Verifica se o campo possui o caminho do arquivo de movimento a ser convertido.
if values[6]:
    #print('Existe!')    
    file_movimento = open(values[6], encoding='latin-1')
    exporta_movimento(file_movimento)

window.close()
