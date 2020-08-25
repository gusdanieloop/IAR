from random import random, randint
import pygame

with open("mapa2.txt") as f:
    tipo_mapa = int(f.readline().strip())
    iteracoes = int(f.readline().strip())
    qtd_agentes = int(f.readline().strip())
    visao = int(f.readline().strip())
    alpha = float(f.readline().strip())

with open(f"data{tipo_mapa}.txt") as f:
    conteudo = f.readlines()

conteudo = [list(map(float, x.strip().split())) for x in conteudo]
N = int(((len(conteudo))/0.10)**0.5)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 000, 255)

values = [0, 255, 128]
colors = []
for r in values:
    for g in values:
        for b in values:
            colors.append((r, g, b))


MARGIN = 2
WIDTH = 600 / N - MARGIN
HEIGHT = 600 / N - MARGIN
WINDOW_SIZE = [600, 600]


###MAPA###
def mapa(N):
    return [[[] for _ in range(N)] for _ in range(N)]

def showMapa(itens):
    print('####################')
    for x in itens:
        for y in x:
            if y != []:
                print(int(y[2]), end=' ')
            else:
                print(end = ' ')
        print()
    print('####################')
            
itens = mapa(N)


for item in conteudo:
    x = y = 0
    while(itens[x][y] != []):
        x = int(random() * N)
        y = int(random() * N)
    itens[x][y] = item

showMapa(itens)

###FORMULAS###

def distanciaEuclidiana(item_a, item_b):
    #print(item_a, item_b)
    return ((item_a[0] - item_b[0])**2 + (item_a[1] - item_b[1])**2)**0.5

def similaridade(x, y, item):
    x = [*range(x - visao, x + visao)]
    y = [*range(y - visao, y + visao)]
    f = 0.0
    for posx in x:
        for posy in y:
            x_ = posx % N
            y_ = posy % N
            if itens[x_][y_] != [] and itens[x_][y_] != item:
                f += (1 - distanciaEuclidiana(item, itens[x_][y_])/ alpha)
    return max(0,f/4)

def pegar(similaridade):
    if similaridade <= 1:
        return 1.0
    return 1/(similaridade**2)

def largar(similaridade):
    if similaridade >= 1:
        return 1.0
    return similaridade**4

class Agente():
    def __init__(self, num, alpha):
        self.num = num
        self.x = int(random() * N)
        self.y = int(random() * N)
        self.carregando = None
        self.alpha = alpha
        self.nfail = 0

    def mover(self):
        self.x = (self.x + randint(-1,1)) % N
        self.y = (self.y + randint(-1,1)) % N
        
    def interagir(self):
        while(True):
            self.mover()
            item = itens[self.x][self.y]
            if item and not self.carregando:
                if pegar(similaridade(self.x, self.y, item)) > random():
                    self.carregando = itens[self.x][self.y]
                    itens[self.x][self.y] = []
                    break
                else:
                    self.nfail += 1
            elif not item and self.carregando:
                if largar(similaridade(self.x, self.y, self.carregando)) > random():
                    itens[self.x][self.y] = self.carregando
                    self.carregando = []
                    break
                else:
                    self.nfail += 1

    def updatealpha(self):
        if self.nfail / 10 > 0.99:
            self.alpha += 0.01
        else:
            self.alpha -= 0.01
        self.nfail = 0


agentes = [Agente(num, alpha) for num in range(qtd_agentes)]

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Dados")
clock = pygame.time.Clock()

screen.fill(BLACK)

inicio = 0
meio = iteracoes // 2
fim = iteracoes - 1

for i in range(iteracoes):
    for agente in agentes:
        agente.interagir()
        if not i % 10:
            agente.updatealpha()
    if not i%10:
        for x in range(N):
            for y in range(N):
                color = BLACK
                if itens[x][y] != []:
                    tipo = itens[x][y][2]
                    color = colors[int(tipo)]
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * y + MARGIN,
                                  (MARGIN + HEIGHT) * x + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        clock.tick(120)
    pygame.display.flip()
    print(i, inicio, meio, fim)
    if i == inicio:
        pygame.image.save(screen, f'./mapa_{tipo_mapa}_inicio.png')
    elif i == meio:
        pygame.image.save(screen, f'./mapa_{tipo_mapa}_meio.png')
    elif i == fim:
        pygame.image.save(screen, f'./mapa_{tipo_mapa}_fim.png')

pygame.quit()