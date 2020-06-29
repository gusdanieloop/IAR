from classe import Mapa
import random

with open("mapa.txt","r+") as arq:
    linha, coluna = map(int,arq.readline().split(" "))
    corpos = float(arq.readline())
    agentes = float(arq.readline())

tam_mapa = linha*coluna
qtd_corpos = int(tam_mapa*corpos)
qtd_agentes = int(tam_mapa*agentes)

mapa = Mapa(linha, coluna, qtd_corpos, qtd_agentes, tam_mapa)
print(mapa.getAgentes(0).getX(), mapa.getAgentes(0).getY())
mapa.getAgentes(0).mover()
print(mapa.getAgentes(0).getX(), mapa.getAgentes(0).getY())

#mapa.show_mapa()

# for i in range():
#     while(True):
#         x = random.randint(0, linha-1)
#         y = random.randint(0, coluna-1)
#         if mapa[x][y] == 0:
#             mapa[x][y] = 2
#             break