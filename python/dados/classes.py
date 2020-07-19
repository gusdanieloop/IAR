import random
import math

class Dado:
    def __init__(self, dados):
        self.dados = [ float(c.replace(',','.')) for c in dados[:-1]]
        self.tipo = dados[-1]
    
    def getDados(self):
        return self.dados

    def getTipo(self):
        return self.tipo

    def getDistancia(self, other):
        soma = 0
        #print(f'dados esse: {self.dados}')
        #print(f'dados outro: {other.getDados()}')
        dados_other = other.getDados()
        for i, dado in enumerate(self.dados):
            soma += ((dado - dados_other[i]) ** 2)
            #soma += ((float(dado.replace(',','.')) - float(dados_other[i].replace(',','.'))) ** 2)
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
            if x >= 0 and y >= 0 and x < self.mapa.linhas and y < self.mapa.colunas:
                self.x = x
                self.y = y
                break

    def interagir(self):
        a = self.mapa.getLocal(self.x, self.y)
        if self.carregando:
            if not a:
                rand = random.random()
                #print(f'chance largar = {self.largar(self.verificar(a))}, {rand}')
                #print()
                if self.largar(self.verificar(a)) > random.random():
                    self.mapa.largar(self.x, self.y, self.carregando)
                    self.carregando = None
        else:
            if a:
                if self.pegar(self.verificar(a)) >= random.random():
                    self.carregando = self.mapa.pegar(self.x, self.y)
        self.mover()
    
    # def verificar(self, dado):
    #     if not dado:
    #         dado = self.carregando
    #     dados_vizinhos = []
    #     tamanho = 0
    #     min_x = max(0, self.x - self.visao)
    #     min_y = max(0, self.y - self.visao)
    #     max_x = min(self.x + self.visao, self.mapa.linhas - 1)
    #     max_y = min(self.y + self.visao, self.mapa.colunas - 1)
    #     for i in range(min_x, max_x+1):
    #         for j in range(min_y, max_y+1):
    #             if self.mapa.mapa[i][j] and i != self.x and j != self.y:
    #                 dados_vizinhos.append(self.mapa.mapa[i][j])
    #             tamanho+=1
    #     return self.similaridade(dado, dados_vizinhos, tamanho)

    def verificar(self, dado):
        if not dado:
            dado = self.carregando
        qtd_corpos = 0
        qtd_blocos = 0
        dados_vizinhos = []
        for i in range(-self.visao, self.visao + 1):
            for j in range(-self.visao, self.visao + 1):
                x = self.x + i
                y = self.y + j
                if((x >= 0 and x < self.mapa.linhas) and y >= 0 and y < self.mapa.colunas and self.mapa.mapa[x][y] != 0 and x != self.x and y != self.y):
                    dados_vizinhos.append(self.mapa.mapa[x][y])
                    qtd_blocos += 1
        #self.setProporcao((qtd_corpos-1)/(qtd_blocos))
        #self.setQtd_corpos(qtd_corpos)
        return self.similaridade(dado, dados_vizinhos, qtd_blocos)

    
    def similaridade(self, dado, dados_vizinhos, tamanho):
        if not tamanho:
            return 0
        escala = self.mapa.getEscala()
        #f = sum([(1 - (dado.getDistancia(dv) / self.mapa.getEscala())) for dv in dados_vizinhos]) / tamanho 
        #print(f'escala = {escala}, tamanho = {tamanho}')
        #f = sum([(1 - ((dado.getDistancia(dv) / escala))) for dv in dados_vizinhos]) / tamanho
        f = 0
        for dv in dados_vizinhos:
            #print(f'dado = {dado.getDistancia(dv)}')
            f+=(1 - ((dado.getDistancia(dv) / escala)))
        f/=tamanho
        #print(f'f = {f}')
        #print(f'vizinhos = {len(dados_vizinhos)}')
        #print(f'similaridade {f} -- pos {self.x} {self.y}')
        # self.mapa.showMapa()
        return max(0, f)

    def pegar(self, similar):
        return (self.mapa.k1 / ( self.mapa.k1 + similar))**2

    def largar(self, similar):
        return (similar / (self.mapa.k2 + similar))**2

    def getCarregando(self):
        return self.carregando



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
        self.k1 = None
        self.k2 = None

        self.construirMapa()
        self.preencherMapa()
        self.construirEscalaDissimilaridade()
        self.construirKs()
        self.construirAgentes(visao)

    def construirEscalaDissimilaridade(self):
        maximo = max(self.conteudo)
        minimo = min(self.conteudo)
        media = 0
        for i in range(len(maximo)-1):
            media += ((float(maximo[i].replace(',','.')) - float(minimo[i].replace(',','.')))**2)
        media = media ** 0.5
        media /= 2
        # print(f'media escala: {media}')
        self.escala_dissimilaridade = media 
        #self.escala_dissimilaridade = random.random()  

    def construirKs(self):
        self.k1 = random.random()
        self.k2 = random.random()
        # print(f'k1: {self.k1} k2: {self.k2}')
 
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
                    #print('0', end=' ')
                    print(end = ' ')
            print()

    def construirAgentes(self, visao):
        for i in range(self.qtd_agentes):
            x = random.randint(0, self.linhas - 1)
            y = random.randint(0, self.colunas - 1)
            self.agentes.append(Agente(x, y, visao, self))

    def getEscala(self):
        return self.escala_dissimilaridade

    def getAgente(self, pos):
        return self.agentes[pos]

    def getLocal(self, x, y):
        return self.mapa[x][y]

    def largar(self, x, y, dado):
        self.mapa[x][y] = dado

    def pegar(self, x, y):
        dado = self.mapa[x][y]
        self.mapa[x][y] = 0
        return dado
    
    def agentes_carregando(self):
        carregando = []
        for agente in self.agentes:
            if agente.carregando:
                carregando.append(agente)
        return carregando
    
