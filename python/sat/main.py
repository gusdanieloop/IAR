import random
import copy
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import k
import numpy.random as rn

### 20
with open('3-SAT-instances/uf20-01.cnf') as f:
    arq = f.readlines()

_, _, nvar, nclauses = arq[7].split()
nvar = int(nvar)
nclauses = int(nclauses)

current_answer = [(random.randint(-1,1) == 0) for i in range(int(nvar))]
clauses = [list(map(int,x.split()[:-1])) for x in arq[8:] if len(x.split()) > 3]
'''
print(current_answer)

print("#######")

print(clauses)

print("#######")
'''
it = 250000
iterations = 100
temperature = 100
min_temperature = 1
cooling = 0.85


def testClause(clause, answer):
    for x in clause:
        if( (x < 0 and not answer[abs(x)-1]) or (x > 0 and answer[abs(x)-1]) ):
            return True
    return False
         
def percent(nclauses, clauses, answer): #quero maximizar isso aqui
    cont = 0
    for clause in clauses:
        if testClause(clause, answer):
            cont += 1
    return cont#float(cont)/nclauses

def neighbour(nvar, current_answer):
    x = random.randint(0, int(nvar)-1)
    #print(x)
    new_answer = copy.deepcopy(current_answer)
    val = current_answer[x]
    new_answer[x] = not val
    return new_answer

def random_search(nvar, current_answer, nclauses, clauses, iterations):
    s_out = current_answer
    s_out_FO = percent(nclauses, clauses, s_out)
    historico = [s_out_FO]
    for i in range(iterations):
        s = neighbour(nvar, s_out)
        s_FO = percent(nclauses, clauses, s)
        if s_FO > s_out_FO:
            s_out = s
            s_out_FO = s_FO
        historico.append(s_out_FO)
    return s_out, s_out_FO, historico

def simulated_annealing(nvar, current_answer, nclauses, clauses, iterations, temperature, min_temperature, cooling):
    best_answer = current_answer
    percent_best = percent(nclauses, clauses, best_answer)
    #print(percent_best)
    best_temperature = temperature
    historico_temp = [temperature]
    historico_percent = [percent_best]
    cont = 0
    #iterationsaux = iterations
    while(temperature > min_temperature and cont < 2500):
        #print(f'temperatura: {temperature}')
        #iterations = iterationsaux
        #while(iterations > 0):
        for i in range(100):
            neighbour_answer = neighbour(nvar, current_answer)
            #print(current_answer, neighbour_answer)
            percent_neighbour = percent(nclauses, clauses, neighbour_answer)
            percent_current = percent(nclauses, clauses, current_answer)
            #print(f"###percent_neighbour {percent_neighbour} -- percent_current {percent_current} -- {percent_neighbour > percent_current}")
            if(percent_neighbour > percent_current):
                current_answer = neighbour_answer
                percent_current = percent_neighbour
                #print(f"###percent_neighbour {percent_neighbour} -- percent_best {percent_best} -- {percent_neighbour > percent_best}")
                if percent_current > percent_best:
                    best_answer = neighbour_answer
                    best_temperature = temperature
                    percent_best = percent_current
                    #print(f"X: {best_temperature} Y: {percent_best}")
            else:
                x = random.random()
                exxp = (0 - abs(percent_neighbour - percent_current)) / (temperature)
                if(x < math.exp(exxp)):
                    current_answer = neighbour_answer
                    percent_current = percent_neighbour
                    #print(f"pior X: {temperature} Y: {percent_current}")
                    #iterations-=1
            #historico.append(current_answer)
        historico_temp.append(temperature)
        historico_percent.append(percent_current)
        temperature *= 0.75
        cont+=1
    print(f"X: {best_temperature} Y: {percent_best}")
    return best_temperature, percent_best, historico_temp, historico_percent

#print(current_answer, neighbour(nvar, current_answer))

def simulated_annealing2(nvar, current_answer, nclauses, clauses, iterations, temperature, min_temperature, cooling):
    best_answer = current_answer
    percent_best = percent(nclauses, clauses, best_answer)
    best_temperature = temperature
    #print(f"inicial X: {best_temperature} Y: {percent_best}")
    historico_temp = []
    historico_percent = []
    cont = 0
    cont_pior = 0
    cont_pior_aceito = 0
    #iterationsaux = iterations
    while(temperature >= min_temperature and cont < 250000):
        cont_pior = 0
        cont_pior_aceito = 0
        #print(f'temperatura: {temperature}')
        #iterations = iterationsaux
        #while(iterations > 0):
        for i in range(100):
            neighbour_answer = neighbour(nvar, current_answer)
            #print(current_answer, neighbour_answer)
            percent_neighbour = percent(nclauses, clauses, neighbour_answer)
            percent_current = percent(nclauses, clauses, current_answer)
            delta = percent_neighbour - percent_current
            #print(f"###percent_neighbour {percent_neighbour} -- percent_current {percent_current} -- {percent_neighbour > percent_current}")
            if(delta > 0):
                current_answer = neighbour_answer
                percent_current = percent_neighbour
            if(delta < 0):
                cont_pior+=1
                x = rn.random()
                exxp = 15*delta / (temperature) 
                #print(x, np.exp(exxp))
                if(x < (np.exp(exxp))):
                    current_answer = neighbour_answer
                    percent_current = percent_neighbour
                    cont_pior_aceito +=1
            if(percent_neighbour > percent_best):
                percent_best = percent_neighbour
                best_answer = neighbour_answer
                best_temperature = temperature
                #print(f"X: {best_temperature} Y: {percent_best}")
            if(percent_neighbour == percent_best):
                best_temperature = temperature
        historico_temp.append(temperature)
        historico_percent.append(percent_current)
        #print(f'temperatura {temperature} = {cont_pior} -> {cont_pior_aceito}')
        temperature *= 0.97
        cont+=1
    #print(f"final X: {best_temperature} Y: {percent_best}")
    #print(historico_temp)
    #print(historico_percent)
    return best_temperature, percent_best, historico_temp, historico_percent


p = []
prand = []
a = []
arand = []
for i in range(10):
    best_temperature, best_percent, historico_temp, historico_percent = simulated_annealing2(nvar, current_answer, nclauses, clauses, iterations, temperature, min_temperature, cooling)
    plt.ylabel("clausulas cumpridas")
    plt.xlabel("temperatura")      
    plt.plot(historico_temp[:], historico_percent[:])#, 'o', color='black')
    melhor_porcentagem = max(historico_percent)
    melhor_temp = historico_temp[historico_percent.index(melhor_porcentagem)]
    plt.plot(best_temperature, best_percent , 'ro', label='Melhor Resposta')
    plt.legend()
    plt.xlim(plt.xlim()[::-1])
    plt.savefig(f'plot_uf20_{i+1}_SA')
    plt.clf()
    answerrand, percentagerand, historico = random_search(nvar, current_answer, nclauses, clauses, iterations)
    plt.ylabel("clausulas cumpridas")
    plt.xlabel("iterações")
    plt.plot([i for i in range(len(historico))][:], historico[:])
    melhor_porcentagem = max(historico)
    melhor_temp = historico.index(melhor_porcentagem)
    plt.plot(melhor_temp, melhor_porcentagem , 'ro', label='Melhor Resposta')
    plt.legend()
    plt.savefig(f'plot_uf20_{i+1}_RS')
    plt.clf()
    p.append(best_percent)
    prand.append(percentagerand)

print("% CORRECT 20 RS")
print(f'med {np.mean(prand)} desvio {np.std(prand)}')
print("% CORRECT 20 SA")
print(f'med {np.mean(p)} desvio {np.std(p)}');




#print("VARIABLES")
#print(answer)
#print("% CORRECT")
#print(percentage)

### 100
with open('3-SAT-instances/uf100-01.cnf') as f:
    arq = f.readlines()

_, _, nvar, nclauses = arq[7].split()
nvar = int(nvar)
nclauses = int(nclauses)

current_answer = [random.randint(0,1) for i in range(int(nvar))]
clauses = [list(map(int,x.split()[:-1])) for x in arq[8:] if len(x.split()) > 3]

p = []
prand = []
a = []
arand = []
for i in range(10):
    best_temperature, best_percent, historico_temp, historico_percent = simulated_annealing2(nvar, current_answer, nclauses, clauses, iterations, temperature, min_temperature, cooling)
    plt.ylabel("clausulas cumpridas")
    plt.xlabel("temperatura")
    plt.plot(historico_temp[:], historico_percent[:])
    melhor_porcentagem = max(historico_percent)
    melhor_temp = historico_temp[historico_percent.index(melhor_porcentagem)]
    plt.plot(melhor_temp, melhor_porcentagem , 'ro', label='Melhor Resposta')
    plt.legend()
    plt.xlim(plt.xlim()[::-1])
    plt.savefig(f'plot_uf100_{i+1}_SA')
    plt.clf()
    answerrand, percentagerand, historico = random_search(nvar, current_answer, nclauses, clauses, iterations)
    plt.ylabel("clausulas cumpridas")
    plt.xlabel("iterações")
    plt.plot([i for i in range(len(historico))][:], historico[:])
    melhor_porcentagem = max(historico)
    melhor_temp = historico.index(melhor_porcentagem)
    plt.plot(melhor_temp, melhor_porcentagem , 'ro', label='Melhor Resposta')
    plt.legend()
    plt.savefig(f'plot_uf100_{i+1}_RS')
    plt.clf()
    p.append(best_percent)
    prand.append(percentagerand)

print("% CORRECT 100 RS")
print(f'med {np.mean(prand)} desvio {np.std(prand)}')
print("% CORRECT 100 SA")
print(f'med {np.mean(p)} desvio {np.std(p)}');


### 250

with open('3-SAT-instances/uf250-01.cnf') as f:
    arq = f.readlines()

_, _, nvar, nclauses = arq[7].split()
nvar = int(nvar)
nclauses = int(nclauses)

current_answer = [random.randint(0,1) for i in range(int(nvar))]
clauses = [list(map(int,x.split()[:-1])) for x in arq[8:] if len(x.split()) > 3]

p = []
prand = []
a = []
arand = []
for i in range(10):
    best_temperature, best_percent, historico_temp, historico_percent = simulated_annealing2(nvar, current_answer, nclauses, clauses, iterations, temperature, min_temperature, cooling)
    plt.ylabel("clausulas cumpridas")
    plt.xlabel("temperatura")
    plt.plot(historico_temp[:], historico_percent[:])
    melhor_porcentagem = max(historico_percent)
    melhor_temp = historico_temp[historico_percent.index(melhor_porcentagem)]
    plt.plot(melhor_temp, melhor_porcentagem , 'ro', label='Melhor Resposta')
    plt.legend()
    plt.xlim(plt.xlim()[::-1])
    plt.savefig(f'plot_uf250_{i+1}_SA')
    plt.clf()
    answerrand, percentagerand, historico = random_search(nvar, current_answer, nclauses, clauses, iterations)
    plt.ylabel("clausulas cumpridas")
    plt.xlabel("iterações")
    plt.plot([i for i in range(len(historico))][:], historico[:])
    melhor_porcentagem = max(historico)
    melhor_temp = historico.index(melhor_porcentagem)
    plt.plot(melhor_temp, melhor_porcentagem , 'ro', label='Melhor Resposta')
    plt.legend()
    plt.savefig(f'plot_uf250_{i+1}_RS')
    plt.clf()
    p.append(best_percent)
    prand.append(percentagerand)

print("% CORRECT 250 RS")
print(f'med {np.mean(prand)} desvio {np.std(prand)}')
print("% CORRECT 250 SA")
print(f'med {np.mean(p)} desvio {np.std(p)}');
