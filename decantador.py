import requests 
import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def homepage():
  return 'Decantador'

@app.route('/decantador')
def decantador():

  print ('solicitação recebida')
  
  #variaveis de controle
  i_temporepouso = time.time()
  iniciarepouso = 0
  
  while True:

    # ajustando o tempo de repouso do decantador
    arq = open("variaveis.txt", "r")
    conteudo = arq.readlines()
    arq.close()

    if (len(conteudo)>0):
      for linha in conteudo:
        texto = linha.split()
        if (texto[0] == 'qtd_decantador'):
          qtd_decantador = float(texto[2])
        elif (texto[0] == 'repouso'):
          repouso = int(texto[2])

    if (repouso == 1 and iniciarepouso == 0):
      i_temporepouso = time.time()
      iniciarepouso = 1

    f_temporepouso = time.time()-i_temporepouso

    # caso ja esteja repousando a 5 segundos, reativo o decantador
    if (f_temporepouso >= 5.0 and repouso == 1):
      
      arq = open("variaveis.txt", "r")
      conteudo = arq.readlines()
      arq.close()

      if (len(conteudo)>0):
        arq = open("variaveis.txt", "w")
        novo_conteudo = ''
        for linha in conteudo:
          texto = linha.split()
  
          if (texto[0] == 'repouso'):
            valor = 'repouso = 0\n'
            novo_conteudo = novo_conteudo + valor
          else:
            novo_conteudo = novo_conteudo + linha

        arq.write(novo_conteudo)
        arq.close()  
        iniciarepouso = 0

    # envio a solucao para os tanques de lavagem

    if (qtd_decantador >= 5.0):

      # ajustando a saida do decantador
      qtd_glicerina = qtd_decantador*0.01
      qtd_etoh = qtd_decantador*0.03
      qtd_solucao = qtd_decantador*0.96
      
      link = f"https://TanqueLavagem1.unifkaraujo.repl.co/vazaosolucao/{qtd_solucao}"
      requests.get(link)     

      link = f"https://Glicerina.unifkaraujo.repl.co/tanqueglicerina/{qtd_glicerina}"
      requests.get(link) 

      link = f"https://Processo-3-Etoh.unifkaraujo.repl.co/entradaetoh/{qtd_etoh}"
      requests.get(link) 
      
      qtd_decantador = 0

      arq = open("variaveis.txt", "r")
      conteudo = arq.readlines()
      arq.close()

      if (len(conteudo)>0):
        arq = open("variaveis.txt", "w")
        novo_conteudo = ''
        for linha in conteudo:
          texto = linha.split()
  
          if (texto[0] == 'qtd_decantador'):
            valor = 'qtd_decantador = 0\n'
            novo_conteudo = novo_conteudo + valor
          else:
            novo_conteudo = novo_conteudo + linha

        arq.write(novo_conteudo)
        arq.close()

  resposta = {'': 0}
  return jsonify(resposta)

@app.route('/retornaestadodecantador')
def retornaestadodecantador():

  qtd_decantador = 0
  repouso = 1
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_decantador'):
        qtd_decantador = float(texto[2]) 
      elif (texto[0] == 'repouso'):
        repouso = int(texto[2])

  if (qtd_decantador is None):
    qtd_decantador = 0
    repouso = 1
      
  resposta = {'qtd_decantador': qtd_decantador, 'repouso': repouso}
  return jsonify(resposta)

@app.route('/vazaodecantador/<num>')
def vazaodecantador(num):

    arq = open("variaveis.txt", "r")
    conteudo = arq.readlines()
    arq.close()

    if (len(conteudo)>0):
      arq = open("variaveis.txt", "w")
      novo_conteudo = ''
      for linha in conteudo:
          texto = linha.split()
  
          if (texto[0] == 'qtd_decantador'):
            num = float(num) + float(texto[2])
            valor = 'qtd_decantador = ' + str(num) + '\n'
            novo_conteudo = novo_conteudo + valor
          elif (texto[0] == 'repouso' and num==5.0):
            valor = 'repouso = 1\n'
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
  novo_conteudo = 'qtd_decantador = 0 \nrepouso = 0'
  arq.write(novo_conteudo)
  arq.close()
      
  resposta = {'': 0}
  return jsonify(resposta)

@app.route('/retornaqtddecantador')
def retornaqtddecantador():

  qtd_decantador = 0
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_decantador'):
        qtd_decantador = texto[2]

  if (qtd_decantador is None):
    qtd_decantador = 0
      
  resposta = {'qtd_decantador': qtd_decantador}
  return jsonify(resposta)

app.run(host='0.0.0.0')