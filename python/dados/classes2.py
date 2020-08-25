from random import random, randint

class Dado():
    def __init__(self, dados):
        self.dados = list(map(float, dados[:-1]))
        self.tipo = int(dados[-1])

    def dist(self, other):
        soma = 0.0
        dados_other = other.dados
        for i, dado in enumerate(self.dados):
            soma += ((dado - dados_other[i]) ** 2)
        return soma ** 0.5

    def getDados(self):
        return self.dados

    def getTipo(self):
        return self.tipo


class Agente():
    def __init__(self, n, visao, alpha, mapa):
        self.limite = n
        self.x = int(random() * n)
        self.y = int(random() * n)
        self.carregando = None
        self.visao = visao
        self.mapa = mapa
        self.alpha = alpha

    def mover(self):
        self.x = (self.x + randint(-1,1)) % self.limite
        self.y = (self.y + randint(-1,1)) % self.limite

    def interagir(self):
        self.mover()
        local = self.mapa.mapa[self.x][self.y]
        if self.carregando and not local:
            if self.largar(self.avaliar(self.carregando)) > random():
                self.mapa.mapa[self.x][self.y] = self.carregando
                self.carregando = None
        elif not self.carregando and local:
            if self.pegar(self.avaliar(local)) > random():
                self.carregando = self.mapa.mapa[self.x][self.y]
                self.mapa.mapa[self.x][self.y] = None

    def avaliar(self, dado):
        dados_vizinhos = []
        tamanho = 0
        min_x = max(0, self.x - self.visao)
        min_y = max(0, self.y - self.visao)
        max_x = min(self.x + self.visao, self.limite - 1)
        max_y = min(self.y + self.visao, self.limite - 1)
        for i in range(min_x, max_x+1):
            for j in range(min_y, max_y+1):
                if self.mapa.mapa[i][j] and i != self.x and j != self.y:
                    dados_vizinhos.append(self.mapa.mapa[i][j])
                tamanho+=1
        return self.similaridade(dado, dados_vizinhos, tamanho-1)

    def similaridade(self,dado, dados_vizinhos, tamanho):
        f = 0.0
        for item in dados_vizinhos:
            f += max(0, 1 - dado.dist(item)/self.alpha)
        return f/tamanho

    def pegar(self, similar):
        if similar <= 1:
            return 1.0
        return 1/(similar**2)

    def largar(self, similar):
        if similar >= 1:
            return 1.0
        return similar**4


class Mapa():
    def __init__(self, n, conteudo, agentes, visao, alpha):
        self.mapa = [[None for _ in range(n)] for _ in range(n)]
        self.agentes = [Agente(n, visao, alpha, self) for _ in range(agentes)]

        self.preencher(n, conteudo)

    def preencher(self, n, conteudo):
        for item in conteudo:
            while(True):
                x = int(random() * n)
                y = int(random() * n)
                if not self.mapa[x][y]:
                    self.mapa[x][y] = Dado(item)
                    break

    def show(self):
        for linha in self.mapa:
            for item in linha:
                if item:
                    print(item.tipo, end=' ')
                else:
                    print(end = ' ')
            print()
    
    def agentes_ativos(self):
        return [a for a in self.agentes if a.carregando]