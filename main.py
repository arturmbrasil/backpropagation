import util
import numpy as np
import random

class RedeNeural(object):
  def __init__(self):
    #Parametros
    self.quantidadeGeracoes = 200
    self.taxaAprendizado = 0.3
    self.tamanhoVetorZ = 40

    #Tamanho dos vetores de entrada e saida
    self.tamanhoVetorX = 63
    self.tamanhoVetorY = 7

    #Matrizes com os pesos
    self.matrizV = np.zeros((self.tamanhoVetorX, self.tamanhoVetorZ))
    self.matrizW = np.zeros((self.tamanhoVetorZ, self.tamanhoVetorY))

    for x in range(self.tamanhoVetorX):
      for y in range(self.tamanhoVetorZ):
        rand = random.randint(1,5) / 10
        positivoNegativo = random.randint(0,1)
        if(positivoNegativo == 0):
          rand = rand * (-1)
        
        self.matrizV[x][y] = rand

    for x in range(self.tamanhoVetorZ):
      for y in range(self.tamanhoVetorY):
        rand = random.randint(1,5) / 10
        positivoNegativo = random.randint(0,1)
        if(positivoNegativo == 0):
          rand = rand * (-1)
        
        self.matrizW[x][y] = rand

  def treinamento(self, entradas, saidasEsperadas):
    for i in range(self.quantidadeGeracoes):
      print('Geração: ', i)
      for index in range(len(entradas)):
        self.feedforward(entradas[index])
        self.backpropagation(entradas[index], saidasEsperadas[index])

  def feedforward(self, entrada):
    self.zIn = self.somaPonderada(entrada, self.matrizV, self.tamanhoVetorZ)
    self.vetorZ = self.funcaoAtivacao(self.zIn)
    self.yIn = self.somaPonderada(self.vetorZ, self.matrizW, self.tamanhoVetorY)
    self.vetorY = self.funcaoAtivacao(self.yIn)

    return self.vetorY

  def somaPonderada(self, entrada, matrizPesos, tamanhoVetorZ):
    vetorSomaPonderada = [0] * tamanhoVetorZ
    for j in range(tamanhoVetorZ):
      for i in range(len(entrada)):
          vetorSomaPonderada[j] += entrada[i] * matrizPesos[i][j]

    return vetorSomaPonderada

  def funcaoAtivacao(self, zIn):
    saida = [0] * len(zIn)

    for i in range(len(zIn)):
      saida[i] = self.bipolar(zIn[i])

    return saida

  def bipolar(self, n):
    return 2/(1+np.exp(-n)) - 1

  def bipolarLinha(self, n):
    return 0.5 * ((1 + n) * (1 - n))

  def backpropagation(self, entrada, saidaEsperada):
    self.erros = self.correcaoErro(saidaEsperada)
    self.deltaW = self.atualizaPesos(self.erros, self.vetorZ)
    self.jIn = self.somaPonderada(self.erros, self.deltaW, self.tamanhoVetorZ)
    self.vetorJ = self.atualizaJ(self.jIn, self.vetorZ)
    self.deltaV = self.atualizaPesos(self.vetorJ, entrada)

    self.matrizV = self.atualizaMatriz(self.tamanhoVetorX, self.tamanhoVetorZ, self.matrizV, self.deltaV)
    self.matrizW = self.atualizaMatriz(self.tamanhoVetorZ, self.tamanhoVetorY, self.matrizW, self.deltaW)

  def correcaoErro(self, saidaEsperada):
    err = [0] * len(saidaEsperada)
    
    for k in range(len(saidaEsperada)):
      err[k] = (saidaEsperada[k] - self.vetorY[k]) * self.bipolarLinha(self.vetorY[k])
    
    return err
  
  def atualizaPesos(self, erros, z):
    delta = np.zeros((len(erros), len(z)))

    for i in range(len(erros)):
      for j in range(len(z)):
        delta[i][j] = self.taxaAprendizado * erros[i] * z[j]

    return delta

  def atualizaJ(self, j, z):
    err = [0] * len(j)
    for x in range(len(j)):
      err[x] = j[x] * self.bipolarLinha(z[x])

    return err

  def atualizaMatriz(self, t1, t2, matriz, delta):
    matrizAtualizada = np.zeros((t1, t2))

    for i in range(t1):
      for j in range(t2):
        matrizAtualizada[i][j] = matriz[i][j] + delta[j][i]
    
    return matrizAtualizada

  def reconhecerLetras(self, letras, saidasLetras):
    acertos = 0

    for index in range(len(letras)):
        print("Analisando letra:")
        util.printLetra(util.codigoToConteudo(letras[index]))

        self.reconhecida = self.feedforward(letras[index])
        for i in range(len(self.reconhecida)):
          self.reconhecida[i] = int(round(self.reconhecida[i]))
        #print(self.reconhecida)
        print("Saída: ", util.codigoToLetra(self.reconhecida))
        print()
        #print(saidasLetras[index])
        if saidasLetras[index] == self.reconhecida:
          acertos = acertos + 1
    
    print("Percentual de acerto: ", round((acertos / len(saidasLetras)) * 100, 2), "%")
    print("Acertos: ", acertos)

#Organiza as entradas para o treinamento
entradaTreinamento = util.getArquivosLetras()

entradas = []
saidasEsperadas = []

for arquivo in entradaTreinamento:
    saidasEsperadas.append(util.letraToCodigo(list(arquivo.keys())[0]))
    entradas.append(util.conteudoToCodigo(list(arquivo.values())[0]))

#Letras para serem reconhecidas
letras = []
saidasLetras = [] #Serve apenas para contar os acertos. Considera que o resultado esperado é a primeira letra do nome do arquivo
reconhecer = util.getLetrasParaReconhecer()
for arquivo in reconhecer:
    letras.append(util.conteudoToCodigo(list(arquivo.values())[0]))
    saidasLetras.append(util.letraToCodigo(list(arquivo.keys())[0]))


#Inicio treinamento e reconhece as letras
RN = RedeNeural()
print("Treinando...")
RN.treinamento(entradas, saidasEsperadas)
print("Rede treinada com sucesso.")
RN.reconhecerLetras(letras, saidasLetras)