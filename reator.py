import requests
import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def homepage():
  return 'Reator'

@app.route('/reator')

def reator():

  # a ideia é todos os processos receber um tempo
  
  # controle de tempo local
  inicio=1
  i_tempoprocessamento = time.time()
  i_tempovazaodecantador = time.time()
  
  while True:

    # ajustando os tempos
    f_tempoprocessamento = time.time()-i_tempoprocessamento
    f_tempovazaodecantador = time.time()-i_tempovazaodecantador

    # a cada 1 segundo, processo os componentes do reator
    if (inicio==1 or f_tempoprocessamento>=1.0):

      # verifico se o reator ja possui a quantidade de óleo, naoh e etoh suficientes para processar
      arq = open("variaveis.txt", "r")
      conteudo = arq.readlines()
      arq.close()

      if (len(conteudo)>0):
        for linha in conteudo:
          texto = linha.split()
          if (texto[0] == 'qtd_oleo'):
            qtd_oleo = float(texto[2])
          elif (texto[0] == 'qtd_naoh'):
            qtd_naoh = float(texto[2])
          elif (texto[0] == 'qtd_etoh'):
            qtd_etoh = float(texto[2])
          elif (texto[0] == 'modo'):
            modo = int(texto[2])

      # caso tenha a quantidade de todos os componentes, processo tudo no reator e desligo as entradas de oleo, naoh e etoh até que o reator seja esvaziado novamente
      if (modo == 0 and qtd_oleo == 2.5 and qtd_naoh==1.25 and qtd_etoh==1.25):
        qtd_process = 5.0
        link = f"https://reator.unifkaraujo.repl.co/alteraprocess/{qtd_process}"
        requisicao = requests.get(link)
        i_tempoprocessamento=time.time()
        i_tempovazaodecantador=time.time()

    # se tiver componente processado no reator, realizo a vazão para o decantador
    arq = open("variaveis.txt", "r")
    conteudo = arq.readlines()
    arq.close()

    if (len(conteudo)>0):
      for linha in conteudo:
        texto = linha.split()
        if (texto[0] == 'modo'):
          modo = int(texto[2])
        if (texto[0] == 'qtd_process'):
          qtd_process = float(texto[2])

    # vazao para o decantador a cada 1 segundo
    if (qtd_process>=1.0 and modo == 1 and f_tempovazaodecantador>=1.0):
      qtd_vazao = 1

      # verifico se o decantador consegue armazenar
      link = f"https://Decantador.unifkaraujo.repl.co/retornaestadodecantador"
      requisicao = requests.get(link)

      qtd_decantador = float(requisicao.json()['qtd_decantador'])
      repouso = int(requisicao.json()['repouso']) 
      
      # se o decantador não esta em repouso e consegue armazenar, realizo a vazão
      if (repouso == 0 and qtd_decantador<=10.0):
        
        if (10.0 - qtd_decantador < 1.00):
          qtd_vazao = 10.0 - qtd_decantador

        link = f"https://Decantador.unifkaraujo.repl.co/vazaodecantador/{qtd_vazao}"
        requests.get(link)
        i_tempovazaodecantador=time.time()
        qtd_process -= qtd_vazao
        arq = open("variaveis.txt", "r")
        conteudo = arq.readlines()
        arq.close()

        if (len(conteudo)>0):
          arq = open("variaveis.txt", "w")
          novo_conteudo = ''
          for linha in conteudo:
            texto = linha.split()
  
            if (texto[0] == 'qtd_process'):
              valor = 'qtd_process = ' + str(qtd_process) + '\n'
              novo_conteudo = novo_conteudo + valor

            elif (texto[0] == 'modo' and qtd_process == 0.0):
              valor = 'modo = 0\n'
              novo_conteudo = novo_conteudo + valor  
          
            else:
              novo_conteudo = novo_conteudo + linha

          arq.write(novo_conteudo)
          arq.close()

        if (qtd_process == 0.0):
          # reativo as entradas de componentes
          link = f"https://Processo-1-Tanque-de-Oleo.unifkaraujo.repl.co/reiniciareq"
          requests.get(link)
            
          link = f"https://Processo-2-Naoh.unifkaraujo.repl.co/reiniciareq"
          requests.get(link)

          link = f"https://Processo-3-Etoh.unifkaraujo.repl.co/reiniciareq"
          requests.get(link)
        
  resposta = {'': 0}
  return jsonify(resposta)

@app.route('/retornaqtdetoh')
def retornaqtdetoh():

  qtd_etoh = 0
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_etoh'):
        qtd_etoh = texto[2]
      if (texto[0] == 'modo'):
        modo = texto[2]

  if (qtd_etoh is None):
    qtd_etoh = 0
      
  resposta = {'qtd_etoh': qtd_etoh, 'modo': modo}
  return jsonify(resposta)

@app.route('/retornaqtdnaoh')
def retornaqtdnaoh():

  qtd_naoh = 0
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_naoh'):
        qtd_naoh = texto[2]
      if (texto[0] == 'modo'):
        modo = texto[2]

  if (qtd_naoh is None):
    qtd_naoh = 0
      
  resposta = {'qtd_naoh': qtd_naoh, 'modo': modo}
  return jsonify(resposta)

@app.route('/retornaqtdoleo')
def retornaqtdoleo():

  qtd_oleo = 0
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_oleo'):
        qtd_oleo = texto[2]
      if (texto[0] == 'modo'):
        modo = texto[2]

  if (qtd_oleo is None):
    qtd_oleo = 0
      
  resposta = {'qtd_oleo': qtd_oleo, 'modo': modo}
  return jsonify(resposta)

@app.route('/vazaooleo/<num>')
def vazaooleo(num):

    vazao_oleo = float(num)
    qtd_oleo_reator = -1
    modo_reator = -1
  
    arq = open("variaveis.txt", "r")
    conteudo = arq.readlines()
    arq.close()

    # verifico se o reator consegue armazenar
    if (len(conteudo)>0):
      for linha in conteudo:
        texto = linha.split()
  
        if (texto[0] == 'qtd_oleo'):
          qtd_oleo_reator = float(texto[2])
        elif (texto[0] == 'modo'):
          modo_reator = int(texto[2])

    # para não dar inconsistencias
    if (qtd_oleo_reator is None):
      qtd_oleo_reator = -1
      modo_reator = -1

    if (qtd_oleo_reator < 2.5 and modo_reator==0):
      
      if (2.5 - qtd_oleo_reator < 0.75):
        vazao_oleo = 2.5 - qtd_oleo_reator

      if (len(conteudo)>0):
        arq = open("variaveis.txt", "w")
        novo_conteudo = ''
        for linha in conteudo:
          texto = linha.split()
  
          if (texto[0] == 'qtd_oleo'):
            qtd_oleo = float(vazao_oleo) + float(texto[2])
            valor = 'qtd_oleo = ' + str(qtd_oleo) + '\n'
            novo_conteudo = novo_conteudo + valor
          else:
            novo_conteudo = novo_conteudo + linha

        arq.write(novo_conteudo)
        arq.close()

      resposta = {'vazao_oleo': vazao_oleo}
      return jsonify(resposta)
    elif (qtd_oleo_reator == -1):
      resposta = {'vazao_oleo': -1}
      return jsonify(resposta)
    else:
      resposta = {'vazao_oleo': 0}
      return jsonify(resposta)

@app.route('/vazaonaoh/<num>')
def vazaonaoh(num):

    vazao_naoh = float(num)
    qtd_naoh_reator = -1
    modo_reator = -1
  
    arq = open("variaveis.txt", "r")
    conteudo = arq.readlines()
    arq.close()

    # verifico se o reator consegue armazenar
    if (len(conteudo)>0):
      for linha in conteudo:
        texto = linha.split()
  
        if (texto[0] == 'qtd_naoh'):
          qtd_naoh_reator = float(texto[2])
        elif (texto[0] == 'modo'):
          modo_reator = int(texto[2])

    # para não dar inconsistencias
    if (qtd_naoh_reator is None):
      qtd_naoh_reator = -1
      modo_reator = -1
      
    if (qtd_naoh_reator < 1.25 and modo_reator==0):
      
      if (1.25 - qtd_naoh_reator < 1.00):
        vazao_naoh = 1.25 - qtd_naoh_reator

      if (len(conteudo)>0):
        arq = open("variaveis.txt", "w")
        novo_conteudo = ''
        for linha in conteudo:
          texto = linha.split()
  
          if (texto[0] == 'qtd_naoh'):
            qtd_naoh = float(vazao_naoh) + float(texto[2])
            valor = 'qtd_naoh = ' + str(qtd_naoh) + '\n'
            novo_conteudo = novo_conteudo + valor
          else:
            novo_conteudo = novo_conteudo + linha

        arq.write(novo_conteudo)
        arq.close()

      resposta = {'vazao_naoh': vazao_naoh}
      return jsonify(resposta)
    elif (qtd_naoh_reator == -1):
      resposta = {'vazao_naoh': -1}
      return jsonify(resposta)
    else:
      resposta = {'vazao_naoh': 0}
      return jsonify(resposta)

@app.route('/vazaoetoh/<num>')
def vazaoetoh(num):

    vazao_etoh = float(num)
    qtd_etoh_reator = -1
    modo_reator = -1
  
    arq = open("variaveis.txt", "r")
    conteudo = arq.readlines()
    arq.close()

    # verifico se o reator consegue armazenar
    if (len(conteudo)>0):
      for linha in conteudo:
        texto = linha.split()
  
        if (texto[0] == 'qtd_etoh'):
          qtd_etoh_reator = float(texto[2])
        elif (texto[0] == 'modo'):
          modo_reator = int(texto[2])

    # para não dar inconsistencias
    if (qtd_etoh_reator is None):
      qtd_etoh_reator = -1
      modo_reator = -1
      
    if (qtd_etoh_reator < 1.25 and modo_reator==0):
      
      if (1.25 - qtd_etoh_reator < 1.00):
        vazao_etoh = 1.25 - qtd_etoh_reator

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

      resposta = {'vazao_etoh': vazao_etoh}
      return jsonify(resposta)
    elif (qtd_etoh_reator == -1):
      resposta = {'vazao_etoh': -1}
      return jsonify(resposta)
    else:
      resposta = {'vazao_etoh': 0}
      return jsonify(resposta)

@app.route('/alteraprocess/<num>')
def alteraprocess(num):

    arq = open("variaveis.txt", "r")
    conteudo = arq.readlines()
    arq.close()

    if (len(conteudo)>0):
      arq = open("variaveis.txt", "w")
      novo_conteudo = ''
      for linha in conteudo:
          texto = linha.split()
  
          if (texto[0] == 'modo'):
              valor = 'modo = 1' + '\n'
              novo_conteudo = novo_conteudo + valor
          elif (texto[0] == 'qtd_process'):
              valor = 'qtd_process = ' + str(num) + '\n'
              novo_conteudo = novo_conteudo + valor
          elif (texto[0] == 'qtd_oleo'):
              valor = 'qtd_oleo = 0' + '\n'
              novo_conteudo = novo_conteudo + valor
          elif (texto[0] == 'qtd_naoh'):
              valor = 'qtd_naoh = 0' + '\n'
              novo_conteudo = novo_conteudo + valor
          elif (texto[0] == 'qtd_etoh'):
              valor = 'qtd_etoh = 0' + '\n'
              novo_conteudo = novo_conteudo + valor
          else:
              novo_conteudo = novo_conteudo + linha

      arq.write(novo_conteudo)
      arq.close()

    resposta = {'': 0}
    return jsonify(resposta)

@app.route('/retornainicio')
def retornainicio():

  inicio = 0
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'inicio'):
          inicio = texto[2]

  if (inicio is None):
    inicio = 0
      
  resposta = {'inicio': inicio}
  return jsonify(resposta)

@app.route('/iniciaprocesso')
def iniciaprocesso():

  link = f"https://Processo-1-Tanque-de-Oleo.unifkaraujo.repl.co/zeravalores"
  requests.get(link)
  link = f"https://Processo-2-Naoh.unifkaraujo.repl.co/zeravalores"
  requests.get(link)
  link = f"https://Processo-3-Etoh.unifkaraujo.repl.co/zeravalores"
  requests.get(link)
  link = f"https://Decantador.unifkaraujo.repl.co/zeravalores"
  requests.get(link)
  link = f"https://tanquelavagem1.unifkaraujo.repl.co/zeravalores"
  requests.get(link)
  link = f"https://tanquelavagem2.unifkaraujo.repl.co/zeravalores"
  requests.get(link)
  link = f"https://tanquelavagem3.unifkaraujo.repl.co/zeravalores"
  requests.get(link)
  link = f"https://Secador.unifkaraujo.repl.co/zeravalores"
  requests.get(link)
  link = f"https://Tanquebiodisel.unifkaraujo.repl.co/zeravalores"
  requests.get(link)
  link = f"https://Glicerina.unifkaraujo.repl.co/zeravalores"
  requests.get(link)

  arq = open("variaveis.txt", "w")
  novo_conteudo = 'qtd_oleo = 0 \nqtd_naoh = 0 \nqtd_etoh = 0 \nqtd_process = 0 \nmodo = 0 \ninicio = 1'
  arq.write(novo_conteudo)
  arq.close()
      
  resposta = {'': 0}
  return jsonify(resposta)

@app.route('/validainterrupcao')
def validainterrupcao():

  qtd_oleo = 2.5
  qtd_naoh = 1.25
  qtd_etoh = 1.25
  modo = 1
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_oleo'):
          qtd_oleo = texto[2]
      elif (texto[0] == 'qtd_naoh'):
          qtd_naoh = texto[2]
      elif (texto[0] == 'qtd_etoh'):
          qtd_etoh = texto[2]
      elif (texto[0] == 'modo'):
          modo = texto[2]

  if (qtd_oleo is None):
    qtd_oleo = 2.5
  elif (qtd_naoh is None):
    qtd_naoh = 1.25
  elif (qtd_etoh is None):
    qtd_etoh = 1.25
  elif (modo is None):
    modo = 1
      
  resposta = {'qtd_oleo': qtd_oleo,'qtd_naoh': qtd_naoh,'qtd_etoh': qtd_etoh,'modo': modo}
  return jsonify(resposta)

@app.route('/retornaqtdreator')
def retornaqtdreator():

  qtd_reator = 0
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_process'):
        qtd_reator = texto[2]

  if (qtd_reator is None):
    qtd_reator = 0
      
  resposta = {'qtd_reator': qtd_reator}
  return jsonify(resposta)

app.run(host='0.0.0.0')