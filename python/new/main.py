from classes import Mapa

with open("mapa.txt") as f:
    iteracoes = int(f.readline().strip())
    linhas, colunas = map(int, f.readline().strip().split())
    tam_conteudo = float(f.readline().strip())
    agentes = float(f.readline().strip())
    visao = int(f.readline().strip())

with open("data4.txt") as f:
    conteudo = f.readlines()

conteudo = [x.strip().split() for x in conteudo]

tam_mapa = linhas*colunas
qtd_conteudo = min(int(tam_mapa*tam_conteudo), len(conteudo))
qtd_agentes = int(tam_mapa*agentes)


mapa = Mapa(linhas, colunas, qtd_conteudo, qtd_agentes, conteudo, visao)

mapa.showMapa()