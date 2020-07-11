import random

class Dado:
    def __init__(self, dados):
        self.dados = dados[:-1]
        self.tipo = dados[-1]
    
    def getDados(self):
        return self.dados

    def getTipo(self):
        return self.tipo

    def getDistancia(self, other):
        soma = 0
        dados_other = other.getDados()
        for i, dado in enumerate(self.dados):
            soma += (((dado) - dados_other[i]) ** 2)
        return soma ** 0.5

class Agente:
    def __init__(self, x, y, visao, mapa):
        self.x = x
        self.y = y
        self.visao = visao
        self.mapa = mapa
        self.carregando = None

    def mover(self):
        while(True):
            x_ = random.randint(-1, 1)
            y_ = random.randint(-1, 1)
            x = self.x + x_
            y = self.y + y_
            if x >= 0 and y >= 0 and x < self.mapa.getLinhas() and y < self.mapa.getColunas():
                self.x = x
                self.y = y
                break
    
    def verificar(self, dado = self.carregando):
        dados_vizinhos = []
        min_x = max(0, self.x - self.visao)
        min_y = max(0, self.y - self.visao)
        max_x = min(self.x + self.visao, self.mapa.linhas - 1)
        max_y = min(self.y + self.visao, self.mapa.colunas - 1)
        for i in range(min_x, max_x+1):
            for j in range(min_y, max_y+1):
                if self.mapa.mapa[i][j] and i != self.x and j != self.y:
                    dados_vizinhos.append(self.mapa.mapa[i][j])
        similar = self.similaridade(dado, dados_vizinhos)
        #TODO
    
    def similaridade(self, dado, dados_vizinhos):
        f = sum([(1 - (dado.getDistancia(dv) / self.mapa.getEscala())) for dv in dados_vizinhos]) / len(dados_vizinhos)
        return max(0, f)



class Mapa:
    def __init__(self, linhas, colunas, qtd_conteudo, qtd_agentes, conteudo, visao):
        self.linhas = linhas
        self.colunas = colunas
        self.qtd_conteudo = qtd_conteudo
        self.conteudo = conteudo
        self.qtd_agentes = qtd_agentes
        self.agentes = []
        self.mapa = []
        self.tam_mapa = linhas * colunas
        self.escala_dissimilaridade = None

        self.construirMapa()
        self.preencherMapa()
        self.construirAgentes(visao)

    def construirEscalaDissimilaridade(self):
        maximo = self.conteudo[self.qtd_conteudo][-1]
        soma = sum([i for i in range(1, maximo + 1)]) / maximo
        self.escala_dissimilaridade = soma

    def construirMapa(self):
        for i in range(self.linhas):
            self.mapa.append([])
            for j in range(self.colunas):
                self.mapa[i].append(0)
    
    def preencherMapa(self):
        for i in range(self.qtd_conteudo):
            while(True):
                x = random.randint(0, self.linhas - 1)
                y = random.randint(0, self.colunas - 1)
                if self.mapa[x][y] == 0:
                    self.mapa[x][y] = Dado(self.conteudo[i])
                    break

    def showMapa(self):
        for linha in self.mapa:
            for item in linha:
                if item:
                    print(item.getTipo(), end=' ')
                else:
                    print(end = ' ')
            print()

    def construirAgentes(self, visao):
        for i in range(self.qtd_agentes):
            x = random.randint(0, self.linhas - 1)
            y = random.randint(0, self.colunas - 1)
            self.agentes.append(Agente(x, y, visao, self))

    def getEscala(self):
        return self.escala_dissimilaridade

    
