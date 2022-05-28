import requests
import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def homepage():
  return 'Processo 3 - Tanque de Etoh'

@app.route('/tanqueetoh')
def tanqueetoh():

  print ('solicitação recebida')
  
  # controle de tempo local
  inicio = 1
  inicio_proc = 0
  i_tempochegaetoh = time.time()
  i_tempovazaoetoh = time.time()
  i_interrupcao = time.time()
  iniciavazao = 0
  
  qtd_etoh = 0
  
  while (True):

    inicio_proc = 1

    if (inicio_proc == 1):
      
      # lendo a quantidade de etoh no tanque
      arq = open("variaveis.txt", "r")
      conteudo = arq.readlines()
      arq.close()
      
      if (len(conteudo)>0):
        for linha in conteudo:
          texto = linha.split()
          if (texto[0] == 'qtd_etoh'):
            qtd_etoh = float(texto[2])
          elif (texto[0] == 'vazao'):
            vazao = int(texto[2])
    
      # ajustando os tempos
      f_tempochegaetoh = time.time()-i_tempochegaetoh
      f_interrupcao = time.time()-i_interrupcao

      # entrada do etoh ocorre a cada 1 segundo
      if (inicio==1 or f_tempochegaetoh>=1.0):
        entradaetoh = 0.25
        qtd_etoh += entradaetoh

        if (len(conteudo)>0):
          arq = open("variaveis.txt", "w")
          novo_conteudo = ''
          for linha in conteudo:
            texto = linha.split()
            
            if (texto[0] == 'qtd_etoh'):
              valor = 'qtd_etoh = ' + str(qtd_etoh) + '\n'
              novo_conteudo = novo_conteudo + valor
            else:
              novo_conteudo = novo_conteudo + linha
        
          arq.write(novo_conteudo)
          arq.close()

        i_tempochegaetoh = time.time()

      # a cada 11 segundos valido se o retor não esta parado, mesmo podendo funcionar
      if (f_interrupcao>=11.0):
        i_interrupcao=time.time()
        link = f"https://reator.unifkaraujo.repl.co/validainterrupcao"
        requisicao = requests.get(link) 

        qtd_etoh = float(requisicao.json()['qtd_etoh'])
        modo = float(requisicao.json()['modo'])

        arq = open("variaveis.txt", "r")
        conteudo = arq.readlines()
        arq.close()

        if (len(conteudo)>0):
          for linha in conteudo:
            texto = linha.split()
          if (texto[0] == 'vazao'):
            vazao = int(texto[2])

        if (modo == 0 and qtd_etoh<1.25 and vazao==0):
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
        
      # aguardo 1 segundo para realizar a vazão do etoh
      if (qtd_etoh>=1 and iniciavazao==0):
        i_tempovazaoetoh = time.time()
        iniciavazao=1

      f_tempovazaoetoh = time.time()-i_tempovazaoetoh      

      # vazão de etoh para o reator, 1 litro a cada 1 segundo
      if (f_tempovazaoetoh>=1.0 and iniciavazao==1 and qtd_etoh >= 1 and vazao==1):
        vazao_etoh = 1.0
      
        # verifico se o reator consegue armazenar
        
        link = f"https://reator.unifkaraujo.repl.co/vazaoetoh/{vazao_etoh}"
        requisicao = requests.get(link)

        arq = open("variaveis.txt", "r")
        conteudo = arq.readlines()
        arq.close()
        
        # se conseguimos realizar a vazao, altero as variaveis
        vazao_etoh = float(requisicao.json()['vazao_etoh'])
        if (vazao_etoh>0):
          i_tempovazaoetoh = time.time()
          qtd_etoh -= vazao_etoh

          if (len(conteudo)>0):
            arq = open("variaveis.txt", "w")
            novo_conteudo = ''
            for linha in conteudo:
              texto = linha.split()
            
              if (texto[0] == 'qtd_etoh'):
                valor = 'qtd_etoh = ' + str(qtd_etoh) + '\n'
                novo_conteudo = novo_conteudo + valor
              else:
                novo_conteudo = novo_conteudo + linha

            arq.write(novo_conteudo)
            arq.close()
            
          iniciavazao=0
        elif (vazao_etoh != -1):
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

@app.route('/retornaqtdetohtanque')
def retornaqtdetohtanque():

  qtd_etoh_tanque = 0
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_etoh'):
        qtd_etoh_tanque = texto[2]

  if (qtd_etoh_tanque is None):
    qtd_etoh_tanque = 0
      
  resposta = {'qtd_etoh_tanque': qtd_etoh_tanque}
  return jsonify(resposta)

@app.route('/zeravalores')
def zeravalores():
 
  arq = open("variaveis.txt", "w")
  novo_conteudo = 'qtd_etoh = 0 \nvazao = 1'
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

@app.route('/entradaetoh/<num>')
def entradaetoh(num):
  
  vazao_etoh = float(num)
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    arq = open("variaveis.txt", "w")
    novo_conteudo = ''
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_etoh'):
        qtd_etoh = float(vazao_etoh) + float(texto[2])
        valor = 'qtd_etoh = ' + str(qtd_etoh) + '\n'
        novo_conteudo = novo_conteudo + valor
      else:
        novo_conteudo = novo_conteudo + linha

    arq.write(novo_conteudo)
    arq.close()

  resposta = {'': 0}
  return jsonify(resposta)

app.run(host='0.0.0.0')