import csv
import PySimpleGUI as sg

#update wcont.hist set dshistoricopadrao=REPLACE(dshistoricopadrao, '???', '' ) 

# LightGreen3, Topanga
sg.theme('Topanga')

def new_lay():
    # Carregamento da tela.
    layout = [
            [sg.Text('****** DEFINA ABAIXO AS COLUNAS NO SEU CSV ******', font=('Arial', 10, 'bold'), size=(70, 1) , justification='center')],
            [sg.Text('Devedora', font=('Arial', 10, 'bold'), size=(12, 1), justification='center'), 
            sg.Text('Credora', font=('Arial', 10, 'bold'), size=(12, 1), justification='center'), 
            sg.Text('Data', font=('Arial', 10, 'bold'), size=(12, 1), justification='center'),         
            sg.Text('Valor', font=('Arial', 10, 'bold'), size=(12, 1), justification='center'), 
            sg.Text('Histórico', font=('Arial', 10, 'bold'), size=(12, 1), justification='center')],

            [sg.InputText('A', size=(12, 1), justification='center'), 
             sg.InputText('B', size=(12, 1), justification='center'), 
             sg.InputText('C', size=(12, 1), justification='center'), 
             sg.InputText('D', size=(12, 1), justification='center'), 
             sg.InputText('E', size=(12, 1), justification='center')],

            [sg.Text('1 - Abra o Fortes Contábil.')],
            [sg.Text('2 - Abra o cadastro de planos de contas, liste as contas.')],
            [sg.Text('3 - Clique em "IMPRIMIR".')],
            [sg.Text('4 - Deixe as colunas da forma que estão (Código, Descrição, Reduzido, Natureza).')],
            [sg.Text('5 - Clique em "EXPORTAR CSV".')],
            [sg.Text('6 - Selecione este mesmo arquivo abaixo:".')],

            [sg.Text('P. Contas:', font=('Arial', 10, 'bold'), size=(13, 1)), 
             sg.Input(), 
             sg.FileBrowse(tooltip='Procure seu arquivo clicando aqui.', button_text='Localizar')],

            [sg.Text('Movimentação:', font=('Arial', 10, 'bold'), size=(13, 1)), 
             sg.Input(), 
             sg.FileBrowse(tooltip='Procure seu arquivo clicando aqui.', button_text='Localizar')],

            [sg.Submit(tooltip='Clique para converter.', button_text='Converter'), sg.Cancel(tooltip='Clique para cancelar.', button_text='Cancelar')]]

    return layout

# Barra de títuloda aplicação.
window = sg.Window('Converte plano de contas Fortes para Alterdata.', new_lay()).Finalize()

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
        de_para.update({str(row[0].replace('-', '.')):str(reduzida)})
              
        plano_de_contas.write(row[0].replace('-', '.').ljust(30) + 
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
