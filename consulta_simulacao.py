import time
import requests

 
# quantidade de óleo no tanque
link = f"https://Processo-1-Tanque-de-Oleo.unifkaraujo.repl.co/retornaqtdoleotanque"
requisicao = requests.get(link)
qtd_oleo_tanque = float(requisicao.json()['qtd_oleo_tanque'])
    
# quantidade de naoh no tanque
link = f"https://Processo-2-Naoh.unifkaraujo.repl.co/retornaqtdnaohtanque"
requisicao = requests.get(link)
qtd_naoh_tanque = float(requisicao.json()['qtd_naoh_tanque'])
    
# quantidade de etoh no tanque
link = f"https://Processo-3-Etoh.unifkaraujo.repl.co/retornaqtdetohtanque"
requisicao = requests.get(link)
qtd_etoh_tanque = float(requisicao.json()['qtd_etoh_tanque'])

# quantidade no reator
link = f"https://Reator.unifkaraujo.repl.co/retornaqtdreator"
requisicao = requests.get(link)
qtd_reator = float(requisicao.json()['qtd_reator'])

# quantidade no reator
link = f"https://Decantador.unifkaraujo.repl.co/retornaqtddecantador"
requisicao = requests.get(link)
qtd_decantador = float(requisicao.json()['qtd_decantador'])

# quantidade de glicerina no tanque
link = f"https://Glicerina.unifkaraujo.repl.co/retornaqtdglicerina"
requisicao = requests.get(link)
qtd_glicerina = float(requisicao.json()['qtd_glicerina'])    

# quantidade de solucao no tanque de lavagem 1
link = f"https://TanqueLavagem1.unifkaraujo.repl.co/retornaqtdsolucao"
requisicao = requests.get(link)
qtd_solucao1 = float(requisicao.json()['qtd_solucao'])   

# quantidade de solucao no tanque de lavagem 2
link = f"https://TanqueLavagem2.unifkaraujo.repl.co/retornaqtdsolucao"
requisicao = requests.get(link)
qtd_solucao2 = float(requisicao.json()['qtd_solucao'])      

# quantidade de solucao no tanque de lavagem 3
link = f"https://TanqueLavagem3.unifkaraujo.repl.co/retornaqtdsolucao"
requisicao = requests.get(link)
qtd_solucao3= float(requisicao.json()['qtd_solucao'])

# quantidade no secador
link = f"https://Secador.unifkaraujo.repl.co/retornaqtdsecador"
requisicao = requests.get(link)
qtd_secador = float(requisicao.json()['qtd_secador'])

# quantidade de biodisel produzido
link = f"https://Tanquebiodisel.unifkaraujo.repl.co/retornaqtdbiodisel"
requisicao = requests.get(link)
qtd_biodisel = float(requisicao.json()['qtd_biodisel']) 

print ('Óleo no tanque: ', qtd_oleo_tanque)
print ('Naoh no tanque: ', qtd_naoh_tanque)
print ('Etoh no tanque: ', qtd_etoh_tanque)
print ('Quantidade no reator: ', qtd_reator)
print ('Quantidade no decantador: ', qtd_decantador)
print ('Quantidade de glicerina produzida: ', qtd_glicerina)
print ('Solução no tanque de lavagem 1: ', qtd_solucao1)
print ('Solução no tanque de lavagem 2: ', qtd_solucao2)
print ('Solução no tanque de lavagem 3: ', qtd_solucao3)
print ('Quantidade no secador: ', qtd_secador)
print ('Quantidade de biodisel produzido: ', qtd_biodisel)
print ('\n\n')