from classes2 import Mapa
import sys

with open("mapa.txt") as f:
    iteracoes = int(f.readline().strip())
    linhas, colunas = map(int, f.readline().strip().split())
    tam_conteudo = float(f.readline().strip())
    agentes = float(f.readline().strip())
    visao = int(f.readline().strip())

with open("data15.txt") as f:
    conteudo = f.readlines()

conteudo = [x.strip().split() for x in conteudo]

tam_mapa = linhas*colunas
qtd_conteudo = min(int(tam_mapa*tam_conteudo), len(conteudo))
qtd_agentes = int(tam_mapa*agentes)


mapa = Mapa(linhas, colunas, qtd_conteudo, qtd_agentes, conteudo, visao)


original_stdout = sys.stdout
with open('mapa_antes.txt', 'w') as f:
    sys.stdout = f
    mapa.showMapa()
    sys.stdout = original_stdout


for i in range(iteracoes):
    for i in range(qtd_agentes):
        #print(f"iterações {i}")
        mapa.getAgente(i).interagir()

mapa.showMapa()

carregando = mapa.agentes_carregando()
cont = 0
print(f'falta {len(carregando)}')
while(carregando):
    cont+=1
    for i, agente in enumerate(carregando):
        #print(f"carregando = {cont}")
        agente.interagir()
        if not agente.getCarregando():
            carregando.pop(i)
            print('-1')

original_stdout = sys.stdout
with open('mapa_depois.txt', 'w') as f:
    sys.stdout = f
    mapa.showMapa()
    sys.stdout = original_stdout