!pip install -q pyomo
!apt-get install -y -qq glpk-utils

import pyomo.environ as pyEnv

lucros = [15, 65, 98, 35, 45, 47, 21, 26, 37, 18]
pesos = [17, 55, 61, 37, 77, 41, 22, 26, 34, 10]
capacidade = 190
m = len(lucros)

modelo = pyEnv.ConcreteModel()

modelo.Indices = range(m)
modelo.Variaveis = pyEnv.Var(modelo.Indices, within = pyEnv.Binary)
modelo.Objetivo = pyEnv.Objective(expr = sum(lucros[i]*modelo.Variaveis[i] for i in modelo.Indices), sense = pyEnv.maximize)
modelo.Restricoes = pyEnv.Constraint(expr = sum(pesos[i]*modelo.Variaveis[i] for i in modelo.Indices) <= capacidade)

solver = pyEnv.SolverFactory('glpk', executable = '/usr/bin/glpsol')
result_objetivo = solver.solve(modelo, tee = True)

lista = list(modelo.Variaveis.keys())
print()
print()
print('Variaveis: ')
print()
for i in lista:
  print(i, '---', modelo.Variaveis[i]())
print()
print('Valor da função objetivo =', modelo.Objetivo())
