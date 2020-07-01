import pyomo.environ as pyEnv

pesos = [[1, 0, 0, 3, 1],
         [1, 0, 2, 1, 0],
         [1, 1, 0, 0, 0],
         [0, 2, 0, 1, 2],
         [0, 0, 1, 0, 1]]

capacidades = [10, 12, 15, 31, 17]

m = len(capacidades)
n = len(capacidades)

modelo = pyEnv.ConcreteModel()

modelo.Indices = range(m)
modelo.Indices2 = range(n)

modelo.Variaveis = pyEnv.Var(modelo.Indices, within = pyEnv.NonNegativeIntegers)

modelo.Objetivo = pyEnv.Objective(expr = sum(modelo.Variaveis[i] for i in modelo.Indices),
                                  sense = pyEnv.minimize)

def rest(modelo, i):
    return sum(pesos[i][j]*modelo.Variaveis[j] for j in modelo.Indices2) >= capacidades[i]


modelo.rest = pyEnv.Constraint(modelo.Indices, rule = rest)

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
