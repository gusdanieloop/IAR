import random
import copy
import math
import numpy as np
import matplotlib.pyplot as plt

### 20
with open('3-SAT-instances/uf20-01.cnf') as f:
    arq = f.readlines()

_, _, nvar, nclauses = arq[7].split()
nvar = int(nvar)
nclauses = int(nclauses)

current_answer = [(random.randint(0,1) == 0) for i in range(int(nvar))]
clauses = [list(map(int,x.split()[:-1])) for x in arq[8:] if len(x.split()) > 3]
'''
print(current_answer)

print("#######")

print(clauses)

print("#######")
'''
it = 1000
iterations = 100
temperature = 100
min_temperature = 0.1
cooling = 0.75


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
    return float(cont)/nclauses

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
    for i in range(iterations):
        s = neighbour(nvar, s_out)
        s_FO = percent(nclauses, clauses, s)
        if s_FO > s_out_FO:
            s_out = s
            s_out_FO = s_FO
    return s_out, s_out_FO

def simulated_annealing(nvar, current_answer, nclauses, clauses, iterations, temperature, min_temperature, cooling):
    best_answer = current_answer
    percent_best = percent(nclauses, clauses, best_answer)
    #print(percent_best)
    best_temperature = temperature
    historico_temp = [temperature]
    historico_percent = [percent_best]
    cont = 0
    while(temperature > min_temperature and cont < it):
        #print(f'temperatura: {temperature}')
        for i in range(iterations):
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
                    percent_best = percent_neighbour
                    #print(f"X: {besxxt_temperature} Y: {percent_best}")
            else:
                x = random.random()
                exp = (0 - (percent_neighbour - percent_current)) / temperature
                if(x < math.exp(exp)):
                    current_answer = neighbour_answer
                    percent_current = percent_neighbour
            #historico.append(current_answer)
        temperature *= cooling
        historico_temp.append(temperature)
        historico_percent.append(percent_current)
        cont+=1
    return best_temperature, percent_best, historico_temp, historico_percent

#print(current_answer, neighbour(nvar, current_answer))


p = []
prand = []
a = []
arand = []
for i in range(10):
    best_temperature, best_percent, historico_temp, historico_percent = simulated_annealing(nvar, current_answer, nclauses, clauses, iterations, temperature, min_temperature, cooling)
    plt.ylabel("Porcentagem de clausulas cumpridas")
    plt.xlabel("temperatura")
    plt.plot(historico_temp[:], historico_percent[:])
    melhor_porcentagem = max(historico_percent)
    melhor_temp = historico_temp[historico_percent.index(melhor_porcentagem)]
    plt.plot(melhor_temp, melhor_porcentagem , 'ro', label='Melhor Resposta')
    plt.legend()
    plt.xlim(plt.xlim()[::-1])
    plt.savefig(f'plot_uf20_{i+1}')
    plt.clf()
    answerrand, percentagerand = random_search(nvar, current_answer, nclauses, clauses, iterations)
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
    best_temperature, best_percent, historico_temp, historico_percent = simulated_annealing(nvar, current_answer, nclauses, clauses, iterations, temperature, min_temperature, cooling)
    plt.ylabel("Porcentagem de clausulas cumpridas")
    plt.xlabel("temperatura")
    plt.plot(historico_temp[:], historico_percent[:])
    melhor_porcentagem = max(historico_percent)
    melhor_temp = historico_temp[historico_percent.index(melhor_porcentagem)]
    plt.plot(melhor_temp, melhor_porcentagem , 'ro', label='Melhor Resposta')
    plt.legend()
    plt.xlim(plt.xlim()[::-1])
    plt.savefig(f'plot_uf100_{i+1}')
    plt.clf()
    answerrand, percentagerand = random_search(nvar, current_answer, nclauses, clauses, iterations)
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
    best_temperature, best_percent, historico_temp, historico_percent = simulated_annealing(nvar, current_answer, nclauses, clauses, iterations, temperature, min_temperature, cooling)
    plt.ylabel("Porcentagem de clausulas cumpridas")
    plt.xlabel("temperatura")
    plt.plot(historico_temp[:], historico_percent[:])
    melhor_porcentagem = max(historico_percent)
    melhor_temp = historico_temp[historico_percent.index(melhor_porcentagem)]
    plt.plot(melhor_temp, melhor_porcentagem , 'ro', label='Melhor Resposta')
    plt.legend()
    plt.xlim(plt.xlim()[::-1])
    plt.savefig(f'plot_uf250_{i+1}')
    plt.clf()
    answerrand, percentagerand = random_search(nvar, current_answer, nclauses, clauses, iterations)
    p.append(best_percent)
    prand.append(percentagerand)

print("% CORRECT 250 RS")
print(f'med {np.mean(prand)} desvio {np.std(prand)}')
print("% CORRECT 250 SA")
print(f'med {np.mean(p)} desvio {np.std(p)}');
