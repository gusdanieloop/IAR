import pygame
import sys
import time
from collections import defaultdict
from queue import PriorityQueue

PURPLE = (148,0,211)
GOLD = (255,215,0)
BLACK = (0, 0, 0)
GREEN = (124,252,0)
BLUE = (30, 144, 255)
ORANGE = (210, 105, 30)
BROWN = (160,82,45)

colors = [GREEN, BROWN, BLUE, ORANGE]

MARGIN = 1
WIDTH = 600 / 42 - MARGIN
HEIGHT = 600 / 42 - MARGIN
WINDOW_SIZE = [600, 600]

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("ROBO")
clock = pygame.time.Clock()

screen.fill(BLACK)

with open("mapa.txt") as m:
    mapa = m.readlines()

mapa = [list(map(int, x.strip().split())) for x in mapa]
mapa_array = []
for item in mapa:
    mapa_array += item

posx, posy = map(int, input("Digite a posição inicial: ").split())
start = 42*posx + posy
destx, desty = map(int, input("Digite a posição de destino: ").split())
end = 42*destx + desty

global cont_dijkstra 
global cont_aStar 

print(f'start: {start} end: {end}')

class Adjacencia():
    def __init__(self, values):
        self.adj = defaultdict(list) # adj[0] -> [1, 42] 
        self.values = values # mapa.txt em vetor
        self.valueCorreto = {0:1, 1:5,2:10,3:15}
        self.length = 42**2
        self.dist = [sys.maxsize] * (self.length) 
        self.fill()

    def fill(self):
        for i in range(42):
            for j in range(42):
                vizinhos = [(i-1, j),(i, j+1),(i+1,j),(i, j-1)] #vizinhos possiveis: norte leste sul oeste
                vizinhos = [x for x in vizinhos if (x[0] >= 0 and x[0] < 42) and (x[1] >= 0 and x[1] < 42)] #vizinhos ctz: norte leste sul oeste
                for (x,y) in vizinhos:
                    self.adj[42*i + j].append(42*x + y)
    
    def drawMapa(self):
        for s in range(self.length):
            color = colors[self.values[s]]
            pygame.draw.rect(
                screen,
                color,
                [(MARGIN + WIDTH) * (s%42) + MARGIN,
                (MARGIN + HEIGHT) * (s//42) + MARGIN,
                WIDTH,
                HEIGHT]
            )
        clock.tick(120)
        pygame.display.flip()

    def caminho(self,s, color):
        pygame.draw.rect(
            screen,
            color,
            [(MARGIN + WIDTH) * (s%42) + MARGIN,
            (MARGIN + HEIGHT) * (s//42) + MARGIN,
            WIDTH,
            HEIGHT]
        )
        clock.tick(120000)
        time.sleep(0.000000001)
        pygame.display.flip()  

    def bfs(self, visited, start, end):
        self.drawMapa()
        prev = {}
        visited.append(start)
        queue = []
        queue.append(start)
        while(queue):
            s = queue.pop(0)
            #print(f'({s//42},{s%42})', end=' ')
            if s == end:
                return prev
            for neighbour in self.adj[s]:
                if neighbour not in visited:
                    prev[neighbour] = s
                    visited.append(neighbour)
                    queue.append(neighbour)
            color = PURPLE
            self.caminho(s, color)   
                #self.drawMapa()

    def road(self, start, end):
        prev = self.bfs([], start, end)
        whereami = end
        road = [whereami]
        input("Aperte ENTER para continuar")
        self.drawMapa()
        while(whereami != start):
            whereami = prev[whereami]
            road.append(whereami)
        road = [(x, self.valueCorreto[self.values[x]]) for x in road[::-1]]
        color = GOLD
        for item in road:
            self.caminho(item[0], color)
        road2 = [x[1] for x in road]
        return (len(prev), sum(road2))
        #print(f'\n\nroad {road}')

    def distance(self, visited):
        minimo = sys.maxsize
        for i in range(self.length):
            if self.dist[i] < minimo and visited[i] == False:
                minimo = self.dist[i]
                index = i
        return index

    def dijkstra(self, start, end):
        self.drawMapa()
        self.dist[start] = 0
        visited = [False] * (self.length)
        prev = {}
        current = start
        while current != end:
            #print(f"CURRENT: {current}")
            #print(self.dist[:4])
            current = self.distance(visited)
            #print(f'estou em {current}')
            
            for node in self.adj[current]:
                if self.dist[node] > self.dist[current] + self.valueCorreto[self.values[node]] and not visited[node]:
                    prev[node] = current 
                    self.dist[node] = self.dist[current] + self.valueCorreto[self.values[node]]
            visited[current] = True
            color = PURPLE
            self.caminho(current, color)
            #print(f'{current} visitado')
        return prev
    


    def path(self, start, end):
        prev = self.dijkstra(start, end)
        input("Aperte ENTER para continuar")
        self.drawMapa()
        #print('TODOS OS NÓS PERCORRIDOS DIJKSTRA')
        #print(prev)
        #print("passou do dijkstra")
        current = end
        path = [current]
        while current != start:
            current = prev[current]
            path.append(current)
        color = GOLD
        for item in path[::-1]:
            self.caminho(item, color)
        road = [self.valueCorreto[self.values[x]] for x in path[::-1]]
        return (len(prev), sum(road))
        #return path[::-1]


    def dist_manhattan(self, a, b):
        a = (a//42, a%42)
        b = (b//42, b%42)
        #print(a,b)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def astar(self, start, end):
        openset = set()
        g = {}
        g[start] = 0
        h = {}
        h[start] = self.dist_manhattan(end, start)
        openset.add(start) # posicao
        prev = {}
        prev[start] = None
        closedset = set()
        
        while openset:
            current = min(openset, key=lambda x: g[x] + h[x])

            color = PURPLE
            self.caminho(current, color)

            if current == end:
                return prev

            openset.remove(current)
            closedset.add(current)

            for node in self.adj[current]:
                if node in closedset:
                    continue
                if node in openset:
                    new_g = g[current] + self.valueCorreto[self.values[node]]
                    if g[node] > new_g:
                        g[node] = new_g
                        prev[node] = current
                else:
                    g[node] = g[current] + self.valueCorreto[self.values[node]]
                    h[node] = self.dist_manhattan(end, node)
                    prev[node] = current
                    openset.add(node)

    def pathStar(self, start, end):
        #prev = self.aStar(start, end)
        prev = self.astar(start, end)
        #print('TODOS OS NÓS PERCORRIDOS A*')
        #print(prev)
        input("Aperte ENTER para continuar")
        self.drawMapa()
        current = end
        path = [current]
        while current != start:
            current = prev[current]
            path.append(current)
        color = GOLD
        for item in path[::-1]:
            self.caminho(item, color)
        road = [self.valueCorreto[self.values[x]] for x in path[::-1]]
        return (len(prev), sum(road))


adj = Adjacencia(mapa_array)
print('BFS')
bfs = adj.road(start, end)
input('ENTER para continuar com DIJKSTRA')
print('DIJKSTRA')
dij = adj.path(start,end)
input('ENTER para continuar com A*')
print('A*')
#adj.astar(start, end)
ast = adj.pathStar(start,end)
input('ENTER para sair')
pygame.quit()

print("##### RESULTADOS #####")
print(f"Qnt. nós visitados -- BFS: {bfs[0]} - Dijkstra: {dij[0]} - A*: {ast[0]}")
print(f"Custo -- BFS: {bfs[1]} - Dijkstra: {dij[1]} - A*: {ast[1]}")
# print(cont_dijkstra)
# print(cont_aStar)