import requests 
import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def homepage():
  return 'Secador'

@app.route('/secador')
def secador():

  print ('solicitação recebida')
  
  #variaveis de controle
  i_temposecagem = time.time()
  secando = 0
  
  while True:

    # ajustando o tempo de repouso do decantador
    arq = open("variaveis.txt", "r")
    conteudo = arq.readlines()
    arq.close()

    if (len(conteudo)>0):
      for linha in conteudo:
        texto = linha.split()
        if (texto[0] == 'qtd_secador'):
          qtd_secador = float(texto[2])

    if (qtd_secador>=1.0 and secando == 0):
      i_temposecagem = time.time()
      secando = 1

    f_temposecagem = time.time()-i_temposecagem

    # aguardo a secagem de 5 segundos por litro e envio para o tanque de biodisel
    if (f_temposecagem>=5.0 and secando == 1):
      
      # perde 0.5% da solução
      qtd_saida = 1.0
      qtd_vazao = qtd_saida*0.995
      
      # envio para o tanque de biodisel
      link = f"https://Tanquebiodisel.unifkaraujo.repl.co/vazaobiodisel/{qtd_vazao}"
      requests.get(link)
      
      # ajusto os valores no arquivo
      i_temposecagem = time.time()
      secando = 0
      qtd_secador = qtd_secador-qtd_saida
      arq = open("variaveis.txt", "r")
      conteudo = arq.readlines()
      arq.close()

      if (len(conteudo)>0):
        arq = open("variaveis.txt", "w")
        novo_conteudo = ''
        for linha in conteudo:
          texto = linha.split()
  
          if (texto[0] == 'qtd_secador'):
            valor = 'qtd_secador = ' + str(qtd_secador) + '\n'
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
      if (texto[0] == 'qtd_secador'):
        qtd_secador = float(vazao_solucao) + float(texto[2])
        valor = 'qtd_secador = ' + str(qtd_secador) + '\n'
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
  novo_conteudo = 'qtd_secador = 0'
  arq.write(novo_conteudo)
  arq.close()
      
  resposta = {'': 0}
  return jsonify(resposta)

@app.route('/retornaqtdsecador')
def retornaqtdsecador():

  qtd_secador = 0
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_secador'):
        qtd_secador = texto[2]

  if (qtd_secador is None):
    qtd_secador = 0
      
  resposta = {'qtd_secador': qtd_secador}
  return jsonify(resposta)

app.run(host='0.0.0.0')