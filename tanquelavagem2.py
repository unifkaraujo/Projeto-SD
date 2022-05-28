import requests 
import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def homepage():
  return 'Tanque Lavagem 2'

@app.route('/tanquelavagem2')
def tanquelavagem2():

  print ('solicitação recebida')
  
  #variaveis de controle
  i_vazaotanque = time.time()
  
  while True:

    # ajustando o tempo de repouso do decantador
    arq = open("variaveis.txt", "r")
    conteudo = arq.readlines()
    arq.close()

    if (len(conteudo)>0):
      for linha in conteudo:
        texto = linha.split()
        if (texto[0] == 'qtd_solucao'):
          qtd_solucao = float(texto[2])

    f_temposolucao = time.time()-i_vazaotanque

    # envio a solucao de 1,5 litros para o proximo tanque de lavagem a cada 1 segundo
    if (f_temposolucao>=1.0 and qtd_solucao >= 1.5):
      
       # perde 2.5% da solução
      qtd_saida = 1.5
      qtd_vazao = qtd_saida*0.975
      
      # envio para o próximo tanque
      link = f"https://TanqueLavagem3.unifkaraujo.repl.co/vazaosolucao/{qtd_vazao}"
      requests.get(link)      
      
      # ajusto os valores no arquivo
      i_vazaotanque = time.time()
      qtd_solucao = qtd_solucao-qtd_saida
      arq = open("variaveis.txt", "r")
      conteudo = arq.readlines()
      arq.close()

      if (len(conteudo)>0):
        arq = open("variaveis.txt", "w")
        novo_conteudo = ''
        for linha in conteudo:
          texto = linha.split()
  
          if (texto[0] == 'qtd_solucao'):
            valor = 'qtd_solucao = ' + str(qtd_solucao) + '\n'
            novo_conteudo = novo_conteudo + valor
          else:
            novo_conteudo = novo_conteudo + linha

        arq.write(novo_conteudo)
        arq.close()

  resposta = {'': 0}
  return jsonify(resposta)

@app.route('/vazaosolucao/<num>')
def vazaosolucao(num):
  
  vazao_solucao = float(num)
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    arq = open("variaveis.txt", "w")
    novo_conteudo = ''
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_solucao'):
        qtd_solucao = float(vazao_solucao) + float(texto[2])
        valor = 'qtd_solucao = ' + str(qtd_solucao) + '\n'
        novo_conteudo = novo_conteudo + valor
      else:
        novo_conteudo = novo_conteudo + linha

    arq.write(novo_conteudo)
    arq.close()

  resposta = {'': 0}
  return jsonify(resposta)

@app.route('/zeravalores')
def zeravalores():
  
  arq = open("variaveis.txt", "w")
  novo_conteudo = 'qtd_solucao = 0'
  arq.write(novo_conteudo)
  arq.close()
      
  resposta = {'': 0}
  return jsonify(resposta)

@app.route('/retornaqtdsolucao')
def retornaqtdsolucao():

  qtd_solucao = 0
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_solucao'):
        qtd_solucao = texto[2]

  if (qtd_solucao is None):
    qtd_solucao = 0
  
  resposta = {'qtd_solucao': qtd_solucao}
  return jsonify(resposta)

app.run(host='0.0.0.0')