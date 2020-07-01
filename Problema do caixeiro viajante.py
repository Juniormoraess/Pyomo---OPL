import pyomo.environ as pyEnv

custos = [[0, 22.36, 72.11, 60, 82.46],
          [22.36, 0, 50, 53.85, 70.00],
          [72.11, 50, 0, 63.25, 56.57],
          [60, 53.85, 63.25, 0, 28.28],
          [82.46, 70, 56.57, 28.28, 0]]

m = len(custos[0])
n = len(custos[0])

modelo = pyEnv.ConcreteModel()

modelo.Indices = pyEnv.RangeSet(m)
modelo.Indices2 = pyEnv.RangeSet(n)
modelo.Indices3 = pyEnv.RangeSet(2, n)

modelo.Variaveis = pyEnv.Var(modelo.Indices, modelo.Indices2,
                             within = pyEnv.Binary)

modelo.Variaveis2 = pyEnv.Var(modelo.Indices, 
                              within = pyEnv.NonNegativeIntegers, bounds = (0, n-1))

modelo.Custos = pyEnv.Param(modelo.Indices, modelo.Indices2, 
                            initialize = lambda modelo, i, j: custos[i-1][j-1])

modelo.Objetivo = pyEnv.Objective(expr = sum(modelo.Variaveis[i,j]*modelo.Custos[i,j] for i in modelo.Indices for j in modelo.Indices2), 
                                  sense = pyEnv.minimize)

def rest1(modelo, j):
    return sum(modelo.Variaveis[i,j] for i in modelo.Indices2 if i != j) == 1

def rest2(modelo, i):
    return sum(modelo.Variaveis[i,j] for j in modelo.Indices if j != i) == 1

def rest3(modelo, i, j):
    if i != j:
        return modelo.Variaveis2[i] - modelo.Variaveis2[j] + modelo.Variaveis[i, j] * n <= n-1
    else:
        return modelo.Variaveis2[i] - modelo.Variaveis2[j] == 0

modelo.rest1 = pyEnv.Constraint(modelo.Indices, rule = rest1)
modelo.rest2 = pyEnv.Constraint(modelo.Indices2, rule = rest2)
modelo.rest3 = pyEnv.Constraint(modelo.Indices3, modelo.Indices2, rule = rest3)

solver = pyEnv.SolverFactory('glpk')
result_objetivo = solver.solve(modelo, tee=True)

lista = list(modelo.Variaveis.keys())
print()
print()
print('Variaveis: ')
print()
for i in lista:
    print(i, '---', modelo.Variaveis[i]())
print()
print('Valor da função objetivo =', modelo.Objetivo())
print()
