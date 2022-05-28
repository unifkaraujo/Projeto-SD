import requests 
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def homepage():
  return 'Tanque Biodisel'

@app.route('/vazaobiodisel/<num>')
def vazaobiodisel(num):
  
  vazao_biodisel = float(num)
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    arq = open("variaveis.txt", "w")
    novo_conteudo = ''
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_biodisel'):
        qtd_biodisel = float(vazao_biodisel) + float(texto[2])
        valor = 'qtd_biodisel = ' + str(qtd_biodisel) + '\n'
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
  novo_conteudo = 'qtd_biodisel = 0'
  arq.write(novo_conteudo)
  arq.close()
      
  resposta = {'': 0}
  return jsonify(resposta)

@app.route('/retornaqtdbiodisel')
def retornaqtdbiodisel():

  qtd_biodisel = 0
  
  arq = open("variaveis.txt", "r")
  conteudo = arq.readlines()
  arq.close()

  if (len(conteudo)>0):
    for linha in conteudo:
      texto = linha.split()
      if (texto[0] == 'qtd_biodisel'):
        qtd_biodisel = texto[2]

  if (qtd_biodisel is None):
    qtd_biodisel = 0
      
  resposta = {'qtd_biodisel': qtd_biodisel}
  return jsonify(resposta)

app.run(host='0.0.0.0')