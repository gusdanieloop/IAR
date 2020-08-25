from classe import Mapa
import random
import sys

with open("mapa.txt","r+") as arq:
    linha, coluna = map(int,arq.readline().split(" "))
    corpos = float(arq.readline())
    agentes = float(arq.readline())

tam_mapa = linha*coluna
qtd_corpos = int(tam_mapa*corpos)
qtd_agentes = int(tam_mapa*agentes)

mapa = Mapa(linha, coluna, qtd_corpos, qtd_agentes, tam_mapa)
'''print(mapa.getAgentes(0).getX(), mapa.getAgentes(0).getY())
mapa.getAgentes(0).mover()
print(mapa.getAgentes(0).getX(), mapa.getAgentes(0).getY())
'''
#mapa.show_mapa()


original_stdout = sys.stdout
with open('mapa_antes.txt', 'w') as f:
    sys.stdout = f
    mapa.show_mapa()
    sys.stdout = original_stdout

#print("#####################################################")


for i in range(100000):
    #print("i =",i)
    for j in range(qtd_agentes):
        #print("j =", j)
        mapa.getAgentes(j).interagir2()
#mapa.show_mapa()

#print("#####################################################")

carregando = mapa.agentes_carregando()

#nao_carregando = []
while(carregando):
    for i, agente in enumerate(carregando):
        agente.interagir_final()
        if not agente.getCarregando():
            #print(f"Agente {i} não está mais carregando")
            carregando.pop(i)
        #else:
        #   print(f"Agente {i} ainda carregando")
#print("\n\n\n")
#mapa.show_mapa()

original_stdout = sys.stdout
with open('mapa_depois.txt', 'w') as f:
    sys.stdout = f
    mapa.show_mapa()
    sys.stdout = original_stdout