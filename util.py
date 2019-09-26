import os
        
def getArquivosLetras():
    arquivos = []

    directory = os.listdir('letras')
    for file in directory:
        arquivos.append(getConteudo(file, 'letras/'))

    return arquivos

def getLetrasParaReconhecer():
    reconhecer = []

    diretorio = os.listdir('reconhecer')
    for f in diretorio:
        reconhecer.append(getConteudo(f, 'reconhecer/'))

    return reconhecer

def getConteudo(nome_arquivo, path):

    dicionario = {}
    conteudo = []

    arquivo = open(path + nome_arquivo,'r')
    for linha in arquivo:
        for letra in linha:
            if letra != '\n':
                conteudo.append(letra)

    nome = str(nome_arquivo)[:1]
    #dicionario[str(letras[nome]).replace(',', '').replace('[', '').replace(']', '')] = conteudo
    dicionario[nome] = conteudo
    arquivo.close()

    return dicionario        
        
def letraToCodigo(letra):
    letras = {
        "A": [1, -1, -1, -1, -1, -1, -1],
        "B": [-1, 1, -1, -1, -1, -1, -1],
        "C": [-1, -1, 1, -1, -1, -1, -1],
        "D": [-1, -1, -1, 1, -1, -1, -1],
        "E": [-1, -1, -1, -1, 1, -1, -1],
        "J": [-1, -1, -1, -1, -1, 1, -1],
        "K": [-1, -1, -1, -1, -1, -1, 1],
    }

    return letras[letra]

def codigoToLetra(codigo):
    letras = {
        "A": [1, -1, -1, -1, -1, -1, -1],
        "B": [-1, 1, -1, -1, -1, -1, -1],
        "C": [-1, -1, 1, -1, -1, -1, -1],
        "D": [-1, -1, -1, 1, -1, -1, -1],
        "E": [-1, -1, -1, -1, 1, -1, -1],
        "J": [-1, -1, -1, -1, -1, 1, -1],
        "K": [-1, -1, -1, -1, -1, -1, 1],
    }

    for letra in letras:
        if letras[letra] == codigo:
            return letra
    
    return "Erro"

def conteudoToCodigo(conteudo):
    codigos = []

    for letra in conteudo:
        if letra == '#':
            codigos.append(1)
        elif letra == '.':
            codigos.append(-1)
        else:
            codigos.append(0)

    return codigos

def codigoToConteudo(conteudo):
    letras = []

    for codigo in conteudo:
        if codigo == 1:
            letras.append('#')
        elif codigo == -1:
            letras.append('.')
        else:
            letras.append('?')

    return letras

def printLetra(entrada):
    for x in range(63):
        print(entrada[x], end ="")
        if((x+1) % 7 == 0):
            print("\n", end ="")