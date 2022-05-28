import requests
import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def homepage():
  return 'Processo 2 - Tanque de Naoh'

@app.route('/tanquenaoh')
def tanquenaoh():

  print ('solicitação recebida')
  
  # controle de tempo local
  inicio = 1
  inicio_proc = 0
  i_tempocheganaoh = time.time()
  i_tempovazaonaoh = time.time()
  i_interrupcao = time.time()
  iniciavazao = 0
  
  qtd_naoh = 0
  
  while (True):

    inicio_proc = 1
    
    if (inicio_proc == 1):

      # lendo a quantidade de naoh no tanque
      arq = open("variaveis.txt", "r")
      conteudo = arq.readlines()
      arq.close()

      if (len(conteudo)>0):
        for linha in conteudo:
          texto = linha.split()
          if (texto[0] == 'qtd_naoh'):
            qtd_naoh = float(texto[2])
          elif (texto[0] == 'vazao'):
            vazao = int(texto[2])
    
      # ajustando os tempos
      f_tempocheganaoh = time.time()-i_tempocheganaoh
      f_interrupcao = time.time()-i_interrupcao

      # entrada do naoh ocorre a cada 1 segundo
      if (inicio==1 or f_tempocheganaoh>=1.0):
        entradanaoh = 0.5
        qtd_naoh += entradanaoh

        if (len(conteudo)>0):
          arq = open("variaveis.txt", "w")
          novo_conteudo = ''
          for linha in conteudo:
            texto = linha.split()
            
            if (texto[0] == 'qtd_naoh'):
              valor = 'qtd_naoh = ' + str(qtd_naoh) + '\n'
              novo_conteudo = novo_conteudo + valor
            else:
              novo_conteudo = novo_conteudo + linha

          arq.write(novo_conteudo)
          arq.close()

        i_tempocheganaoh = time.time()
        
      # a cada 10 segundos valido se o retor não esta parado, mesmo podendo funcionar
      if (f_interrupcao>=10.0):
        i_interrupcao=time.time()
        link = f"https://reator.unifkaraujo.repl.co/validainterrupcao"
        requisicao = requests.get(link) 

        qtd_naoh = float(requisicao.json()['qtd_naoh'])
        modo = float(requisicao.json()['modo'])

        arq = open("variaveis.txt", "r")
        conteudo = arq.readlines()
        arq.close()

        if (len(conteudo)>0):
          for linha in conteudo:
            texto = linha.split()
          if (texto[0] == 'vazao'):
            vazao = int(texto[2])

        if (modo == 0 and qtd_naoh<1.25 and vazao==0):

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
        
      # aguardo 1 segundo para realizar a vazão do naoh
      if (qtd_naoh>=1 and iniciavazao==0):
        i_tempovazaonaoh = time.time()
        iniciavazao=1
          
      f_tempovazaonaoh = time.time()-i_tempovazaonaoh

      # vazão de naoh para o reator, 1 litro a cada 1 segundo
      if (f_tempovazaonaoh>=1.0 and iniciavazao==1 and qtd_naoh >= 1 and vazao==1):
        vazao_naoh = 1.0
        
        # verifico se o reator consegue armazenar

        # se o reator consegue armazenar, realizo a vazão
        link = f"https://reator.unifkaraujo.repl.co/vazaonaoh/{vazao_naoh}"
        requisicao = requests.get(link)

        arq = open("variaveis.txt", "r")
        conteudo = arq.readlines()
        arq.close()

        # se conseguimos realizar a vazao, altero as variaveis
        if (requisicao is None):
          vazao_naoh = 0
        else:
          vazao_naoh = float(requisicao.json()['vazao_naoh'])
        if (vazao_naoh>0):
          i_tempovazaonaoh = time.time()
          qtd_naoh -= vazao_naoh

          if (len(conteudo)>0):
            arq = open("variaveis.txt", "w")
            novo_conteudo = ''
            for linha in conteudo:
              texto = linha.split()
            
              if (texto[0] == 'qtd_naoh'):
                valor = 'qtd_naoh = ' + str(qtd_naoh) + '\n'
                novo_conteudo = novo_conteudo + valor
              else:
                novo_conteudo = novo_conteudo + linha
                
            arq.write(novo_conteudo)
            arq.close()

          iniciavazao=0
        elif (vazao_naoh != -1):
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

@app.route('/retornaqtdnaohtanque')
def retornaqtdnaohtanque():

  qtd_naoh_tanque = 0
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_naoh'):
        qtd_naoh_tanque = texto[2]

  if (qtd_naoh_tanque is None):
    qtd_naoh_tanque = 0
      
  resposta = {'qtd_naoh_tanque': qtd_naoh_tanque}
  return jsonify(resposta)

@app.route('/zeravalores')
def zeravalores():
 
  arq = open("variaveis.txt", "w")
  novo_conteudo = 'qtd_naoh = 0 \nvazao = 1'
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