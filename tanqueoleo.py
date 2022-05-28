import requests
import time
from flask import Flask, jsonify
from random import uniform

app = Flask(__name__)

@app.route('/')
def homepage():
  return 'Processo 1 - Tanque de óleo'

@app.route('/tanqueoleo')
def tanqueoleo():

  print ('solicitação recebida')
  
  # controle de tempo local
  inicio = 1
  inicio_proc = 0
  i_tempochegaoleo = time.time()
  i_tempovazao = time.time()
  i_interrupcao = time.time()
  
  qtd_tanque = 0
  
  while (True):

    inicio_proc = 1

    if (inicio_proc == 1):

      # lendo a quantidade de óleo no tanque
      arq = open("variaveis.txt", "r")
      conteudo = arq.readlines()
      arq.close()

      if (len(conteudo)>0):
        for linha in conteudo:
          texto = linha.split()
          if (texto[0] == 'qtd_oleo'):
            qtd_tanque = float(texto[2])
          elif (texto[0] == 'vazao'):
            vazao = int(texto[2])

      # ajustando os tempos
      f_tempochegaoleo = time.time()-i_tempochegaoleo
      f_tempovazao = time.time()-i_tempovazao
      f_interrupcao = time.time()-i_interrupcao

      # entrada de oleo ocorre a cada 10 segundos
      if (inicio==1 or f_tempochegaoleo>=10.0):
        entradaoleo = uniform(1,2)
        qtd_tanque += entradaoleo

        if (len(conteudo)>0):
          arq = open("variaveis.txt", "w")
          novo_conteudo = ''
          for linha in conteudo:
            texto = linha.split()
            
            if (texto[0] == 'qtd_oleo'):
              valor = 'qtd_oleo = ' + str(qtd_tanque) + '\n'
              novo_conteudo = novo_conteudo + valor
            else:
              novo_conteudo = novo_conteudo + linha

          arq.write(novo_conteudo)
          arq.close()
      
        i_tempochegaoleo = time.time()

      # a cada 9 segundos valido se o retor não esta parado, mesmo podendo funcionar
      if (f_interrupcao>=9.0):
        i_interrupcao=time.time()
        link = f"https://reator.unifkaraujo.repl.co/validainterrupcao"
        requisicao = requests.get(link) 

        qtd_oleo = float(requisicao.json()['qtd_oleo'])
        modo = float(requisicao.json()['modo'])

        arq = open("variaveis.txt", "r")
        conteudo = arq.readlines()
        arq.close()

        if (len(conteudo)>0):
          for linha in conteudo:
            texto = linha.split()
          if (texto[0] == 'vazao'):
            vazao = int(texto[2])

        if (modo == 0 and qtd_oleo<2.5 and vazao==0):

          if (len(conteudo)>0):
            arq = open("variaveis.txt", "w")
            novo_conteudo = ''
            for linha in conteudo:
              texto = linha.split()
              if (texto[0] == 'vazao'):
                valor = 'vazao = 1\n'
                novo_conteudo = novo_conteudo + valor
              else:
                novo_conteudo = novo_conteudo + linha

            arq.write(novo_conteudo)
            arq.close()
        
      # vazão de óleo para o reator, a cada 1 segundo
      if (f_tempovazao>=1.0 and qtd_tanque >= 0.75 and vazao==1):
        vazao_oleo = 0.75
      
        # verifico se o reator consegue armazenar
      
        # se o reator consegue armazenar, realizo a vazão
                
        link = f"https://reator.unifkaraujo.repl.co/vazaooleo/{vazao_oleo}"
        requisicao = requests.get(link)

        arq = open("variaveis.txt", "r")
        conteudo = arq.readlines()
        arq.close()
        
        # se conseguimos realizar a vazao, altero as variaveis
        if (requisicao is None):
          vazao_oleo = 0
        else:
          vazao_oleo = float(requisicao.json()['vazao_oleo'])
        if (vazao_oleo>0):
          i_tempovazao = time.time()
          qtd_tanque -= vazao_oleo

          if (len(conteudo)>0):
            arq = open("variaveis.txt", "w")
            novo_conteudo = ''
            for linha in conteudo:
              texto = linha.split()
            
              if (texto[0] == 'qtd_oleo'):
                valor = 'qtd_oleo = ' + str(qtd_tanque) + '\n'
                novo_conteudo = novo_conteudo + valor
              else:
                novo_conteudo = novo_conteudo + linha

            arq.write(novo_conteudo)
            arq.close()
            
        elif (vazao_oleo != -1):

          if (len(conteudo)>0):
            arq = open("variaveis.txt", "w")
            novo_conteudo = ''
            for linha in conteudo:
              texto = linha.split()
            
              if (texto[0] == 'vazao'):
                valor = 'vazao = 0\n'
                novo_conteudo = novo_conteudo + valor
              else:
                novo_conteudo = novo_conteudo + linha
          
            arq.write(novo_conteudo)
            arq.close()          

      inicio = 0
    
  resposta = {'': 0}
  return jsonify(resposta)

@app.route('/retornaqtdoleotanque')
def retornaqtdoleotanque():

  qtd_oleo_tanque = 0
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_oleo'):
        qtd_oleo_tanque = texto[2]

  if (qtd_oleo_tanque is None):
    qtd_oleo_tanque = 0
      
  resposta = {'qtd_oleo_tanque': qtd_oleo_tanque}
  return jsonify(resposta)

@app.route('/zeravalores')
def zeravalores():
 
  arq = open("variaveis.txt", "w")
  novo_conteudo = 'qtd_oleo = 0 \nvazao = 1'
  arq.write(novo_conteudo)
  arq.close()
      
  resposta = {'': 0}
  return jsonify(resposta)

@app.route('/reiniciareq')
def reiniciareq():

  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    arq = open("variaveis.txt", "w")
    novo_conteudo = ''
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'vazao'):
        valor = 'vazao = 1\n'
        novo_conteudo = novo_conteudo + valor
      else:
        novo_conteudo = novo_conteudo + linha
  
    arq.write(novo_conteudo)
    arq.close()       
      
  resposta = {'': 0}
  return jsonify(resposta)

app.run(host='0.0.0.0')