def distancia(a, b):
    soma = 0
    for i, item in enumerate(a):
        soma += ((item - b[i]) ** 2)
    print(f'a: {a} b: {b} | distancia: {soma**0.5}')
    return soma ** 0.5

def similaridade(a, b, tamanho):
    f = 0
    for item in b:
        d = distancia(a, item) / 20.0123124123
        f += (1 - d)
        print(f'{f} -- {d}')
    f /= tamanho
    #f = sum([(1 - (distancia(a, c) / 20 )) for c in b]) / tamanho
    return max(0, f)
    #print(f'posicao: {self.x} {self.y}')
    #print(f'similaridade: {similaridade}')

b = [[-18.97565759,	-18.8728999], [-19.96643604, -20.19195195], [-21.51863715, -19.82882077], [-21.83578191, -19.97722901], [-19.3342435, -23.03138668], [-17.29064484,	-20.19931755], [-19.4617676, -20.5007531], [-17.26135506, -20.11268512] ]

a = [-16.00628646, -16.79795313]

c = [[-16.00628646, -16.79795313],[-16.00628646, -16.79795313],[-16.00628646, -16.79795313],[-16.00628646, -16.79795313],[-16.00628646, -16.79795313],[-16.00628646, -16.79795313],[-16.00628646, -16.79795313]]

print(similaridade(a,b,7))

