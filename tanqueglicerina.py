import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def homepage():
  return 'Tanque Glicerina'

@app.route('/tanqueglicerina/<num>')
def tanqueglicerina(num):
  
  vazao_glicerina = float(num)
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    arq = open("variaveis.txt", "w")
    novo_conteudo = ''
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_glicerina'):
        qtd_glicerina = float(vazao_glicerina) + float(texto[2])
        valor = 'qtd_glicerina = ' + str(qtd_glicerina) + '\n'
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
  novo_conteudo = 'qtd_glicerina = 0'
  arq.write(novo_conteudo)
  arq.close()
      
  resposta = {'': 0}
  return jsonify(resposta)

@app.route('/retornaqtdglicerina')
def retornaqtdglicerina():

  qtd_glicerina = 0
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_glicerina'):
        qtd_glicerina = texto[2]

  if (qtd_glicerina is None):
    qtd_glicerina = 0
      
  resposta = {'qtd_glicerina': qtd_glicerina}
  return jsonify(resposta)

app.run(host='0.0.0.0')