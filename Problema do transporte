!pip install -q pyomo
!apt-get install -y -qq glpk-utils

import pyomo.environ as pyEnv

custos_ij = [[162, 247], [117, 193], [131, 185]]
suprimentos = [1000, 1500, 1200]
demandas = [2300, 1400]

m = len(suprimentos)
n = len(demandas)

modelo = pyEnv.ConcreteModel()

modelo.Indices_fabricas = pyEnv.RangeSet(m)
modelo.Indices_clientes = pyEnv.RangeSet(n)

modelo.Variaveis = pyEnv.Var(modelo.Indices_fabricas, modelo.Indices_clientes, within = pyEnv.NonNegativeReals)

modelo.Custo_transporte = pyEnv.Param(modelo.Indices_fabricas, modelo.Indices_clientes, initialize = lambda modelo, i, j: custos_ij[i-1][j-1])
modelo.Suprimentos = pyEnv.Param(modelo.Indices_fabricas, initialize = lambda modelo, i: suprimentos[i-1])
modelo.Demandas = pyEnv.Param(modelo.Indices_clientes, initialize = lambda modelo, j: demandas[j-1])

modelo.Objetivo = pyEnv.Objective(expr = sum(modelo.Variaveis[i,j] * modelo.Custo_transporte[i,j] for i in modelo.Indices_fabricas for j in modelo.Indices_clientes), sense = pyEnv.minimize)

def rest1(modelo, i):
  return sum(modelo.Variaveis[i,j] for j in modelo.Indices_clientes) <= modelo.Suprimentos[i]

def rest2(modelo, j):
  return sum(modelo.Variaveis[i,j] for i in modelo.Indices_fabricas) >= modelo.Demandas[j]

modelo.rest1 = pyEnv.Constraint(modelo.Indices_fabricas, rule = rest1)
modelo.rest2 = pyEnv.Constraint(modelo.Indices_clientes, rule = rest2)

solver = pyEnv.SolverFactory('glpk', executable = '/usr/bin/glpsol')
result_objetivo = solver.solve(modelo, tee = True)

lista = list(modelo.Variaveis.keys())
print()
print()
print()
modelo.Objetivo()
print(result_objetivo)
print()
for i in lista:
  if modelo.Variaveis[i]() != 0:
    print(i, '---', modelo.Variaveis[i]())
print()
print('Valor da função objetivo =', modelo.Objetivo())
