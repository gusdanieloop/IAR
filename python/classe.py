import random
class Mapa:
    def __init__(self, linhas, colunas, qtd_corpos, qtd_agentes, tam_mapa):
       self.linhas = linhas
       self.colunas = colunas
       self.qtd_corpos = qtd_corpos
       self.qtd_agentes = qtd_agentes
       self.mapa = []
       self.agentes = []
       self.tam_mapa = tam_mapa
       
       self.constroi()
       self.preenche_mapa_corpos()
       self.constroi_agentes()

    def getLinhas(self):
        return self.linhas
    
    def setLinhas(self, linhas):
        self.linhas = linhas
    
    def getAgentes(self, index):
        return self.agentes[index]
    
    def getColunas(self):
        return self.colunas
    
    def setColunas(self, colunas):
        self.colunas = colunas
    
    def getCorpos(self):
        return self.corpos
    
    def setCorpos(self, corpos):
        self.corpos = corpos

    def constroi(self):
        for i in range(self.linhas):
            self.mapa.append([])
            for j in range(self.colunas):
                self.mapa[i].append(0)

    def preenche_mapa_corpos(self):
        for i in range(self.qtd_corpos):
            while(True):
                x = random.randint(0, self.linhas-1)
                y = random.randint(0, self.colunas-1)
                if self.mapa[x][y] == 0:
                    self.mapa[x][y] = 1
                    break

    def constroi_agentes(self):
        for i in range(self.qtd_agentes):
            x = random.randint(0, self.linhas - 1)
            y = random.randint(0, self.colunas - 1)
            self.agentes.append(Agente(x, y, 1, self))

    def show_mapa(self):
        for linha in self.mapa:
            print(*linha)
            print()
            
            
class Agente:
    def __init__(self, x, y, visao, mapa):
        self.x = x
        self.y = y
        self.carregando = False
        self.visao = visao
        self.mapa = mapa

    def getX(self):
        return self.x
    
    def setX(self, x):
        self.x = x
    
    def getVisao(self):
        return self.visao
    
    def setVisao(self, visao):
        self.visao = visao

    def getY(self):
        return self.y
    
    def setY(self, y):
        self.y = y
    
    def getCarregando(self):
        return self.carregando
    
    def setCarregando(self, carregando):
        self.carregando = carregando

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

    def maratona(self, x, y):
        if(self.x - x < 0 or self.y - y < 0 or self.x + x >= self.mapa.getLinhas() or self.y + y >=self.mapa.getColunas())
            return False
        return True
    
    def verificar(self):
        qtd_corpos = 0
        sinal = []
        for i in range(self.visao):
            for j in range(self.visao):
                if self.maratona(i, j):

        if self.x == 0:
            if self.y == 0:
                for i in range(self.visao):
                    for j in range()
