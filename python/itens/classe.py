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
            self.agentes.append(Agente(x, y, 3, self))

    def show_mapa(self):
        for linha in self.mapa:
            for item in linha:
                if item:
                    print(item, end = ' ')
                else:
                    print(end=' ')
            #print(*linha)
            print()

    def tirar_corpo(self, x, y):
        self.mapa[x][y] = 0
        
    def colocar_corpo(self, x, y):
        self.mapa[x][y] = 1

    def agentes_carregando(self):
        agentes = []
        for agente in self.agentes:
            if agente.getCarregando():
                agentes.append(agente)
        return agentes

class Agente:
    def __init__(self, x, y, visao, mapa):
        self.x = x
        self.y = y
        self.carregando = False
        self.visao = visao
        self.mapa = mapa
        self.proporcao = 0
        self.qtd_corpos = 0

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

    def getProporcao(self):
        return self.proporcao
    
    def setProporcao(self, proporcao):
        self.proporcao = proporcao

    def getQtd_corpos(self):
        return self.qtd_corpos

    def setQtd_corpos(self, qtd_corpos):
        self.qtd_corpos = qtd_corpos


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
    
    def interagir(self):
        self.verificar_corpos_ao_redor()
        if self.getProporcao() >= 0.35:
            # print("MUITO CORPO")
            if self.carregando:
                # print("CARREGANDO")
                if not self.mapa.mapa[self.x][self.y]:
                    # print("deixou o corpo")
                    # print(f"x = {self.x}, y = {self.y}")
                    self.mapa.colocar_corpo(self.x, self.y)
                    self.carregando = False
                else:
                    # print("TEM FORMIGA AQUI, mover")
                    self.mover()
            else:
                # print("NAO CARREGANDO, MOVER")
                self.mover()
        else:
            self.getProporcao()
            # print("POUCO CORPO")
            if self.carregando:
                # print("CARREGANDO, MOVER")
                self.mover()
            else:
                if self.mapa.mapa[self.x][self.y]:
                    # print("tirou o corpo")
                    # print(f"x = {self.x}, y = {self.y}")
                    self.mapa.tirar_corpo(self.x, self.y)
                    self.carregando = True
                else:
                    # print("moveu")
                    self.mover()

    def interagir2(self):
        self.verificar2_corpos_ao_redor()
        if self.carregando:
            #quero depositar o corpo
            if not self.mapa.mapa[self.x][self.y]: #nao pode ter corpo onde estou!
                if self.getProporcao() >= random.random(): #chance de depositar o corpo
                    self.mapa.colocar_corpo(self.x, self.y)
                    self.carregando = False
                else:
                    self.mover()
            else: 
                self.mover()
        else:
            #quero pegar um corpo
            if self.mapa.mapa[self.x][self.y]: #tem que ter um corpo onde estou!
                if self.getProporcao() < random.random(): #chance de pegar o corpo
                    self.mapa.tirar_corpo(self.x, self.y)
                    self.carregando = True
                else:
                    self.mover()  
            else:
                self.mover()
    
    def interagir_final(self):
        self.verificar_corpos_ao_redor()
        if not self.mapa.mapa[self.x][self.y]:
            if self.getProporcao() >= random.random(): #chance de depositar
                self.mapa.colocar_corpo(self.x, self.y)
                self.carregando = False
            else:
                self.mover()
        else:
            self.mover()
    
    def verificar_corpos_ao_redor(self):
        qtd_corpos = 0
        qtd_blocos = 0
        for i in range(-self.visao, self.visao + 1):
            for j in range(-self.visao, self.visao + 1):
                x = self.x + i
                y = self.y + j
                if((x >= 0 and x < self.mapa.linhas) and y >= 0 and y < self.mapa.colunas):
                    qtd_corpos += self.mapa.mapa[x][y]
                    qtd_blocos += 1
        self.setProporcao((qtd_corpos-1)/(qtd_blocos))
        self.setQtd_corpos(qtd_corpos)

    def verificar2_corpos_ao_redor(self):
        qtd_corpos = 0
        qtd_blocos = 0
        min_x = max(0, self.x - self.visao)
        min_y = max(0, self.y - self.visao)
        max_x = min(self.x + self.visao, self.mapa.linhas - 1)
        max_y = min(self.y + self.visao, self.mapa.colunas - 1)
        for i in range(min_x, max_x+1):
            for j in range(min_y, max_y+1):
                qtd_corpos += self.mapa.mapa[i][j]
                qtd_blocos += 1
        self.setProporcao(qtd_corpos/qtd_blocos)
        self.setQtd_corpos(qtd_corpos)
                        
