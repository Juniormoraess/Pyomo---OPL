## Modelo matemático ##
## Min 162x11 + 247x12 + 117x21 + 193x22 + 131x31 + 185x32 ##
## S.a x11 + x12 ≤ 1000 ##
##     x21 + x22 ≤ 1500 ##
##     x31 + x32 ≤ 1200 ##
##     x11 + x21 + x31 ≥ 2300 ##
##     x12 + x22 + x32 ≥ 1400 ##

## Caso a implementação esteja sendo feita por uma IDE: ##
## Abra o Anaconda Prompt e insira as seguintes chamadas: ##
## conda install -c conda-forge pyomo ##
## conda install -c conda-forge glpk ##
## Após isto desconsidere os comandos das linhas 16 e 17 ##

## Instalação do pyomo e do solver para o colab ##
!pip install -q pyomo
!apt-get install -y -qq glpk-utils

## Importando a biblioteca pyomo ##
import pyomo.environ as pyEnv

## Dados do problema ##
custos_ij = [[162, 247], [117, 193], [131, 185]]
suprimentos = [1000, 1500, 1200]
demandas = [2300, 1400]

m = len(suprimentos)
n = len(demandas)

## Declarando o modelo através da biblioteca ##
modelo = pyEnv.ConcreteModel()

## Criando Indices ##
modelo.Indices_fabricas = pyEnv.RangeSet(m)
modelo.Indices_clientes = pyEnv.RangeSet(n)

## Criando as variáveis ##
modelo.Variaveis = pyEnv.Var(modelo.Indices_fabricas, modelo.Indices_clientes, within = pyEnv.NonNegativeReals)

modelo.Custo_transporte = pyEnv.Param(modelo.Indices_fabricas, modelo.Indices_clientes, initialize = lambda modelo, i, j: custos_ij[i-1][j-1])
modelo.Suprimentos = pyEnv.Param(modelo.Indices_fabricas, initialize = lambda modelo, i: suprimentos[i-1])
modelo.Demandas = pyEnv.Param(modelo.Indices_clientes, initialize = lambda modelo, j: demandas[j-1])

## Criando a Função Objetivo ##
modelo.Objetivo = pyEnv.Objective(expr = sum(modelo.Variaveis[i,j] * modelo.Custo_transporte[i,j] for i in modelo.Indices_fabricas for j in modelo.Indices_clientes), sense = pyEnv.minimize)

## Criando as restrições ##
def rest1(modelo, i):
  return sum(modelo.Variaveis[i,j] for j in modelo.Indices_clientes) <= modelo.Suprimentos[i]

def rest2(modelo, j):
  return sum(modelo.Variaveis[i,j] for i in modelo.Indices_fabricas) >= modelo.Demandas[j]

modelo.rest1 = pyEnv.Constraint(modelo.Indices_fabricas, rule = rest1)
modelo.rest2 = pyEnv.Constraint(modelo.Indices_clientes, rule = rest2)

## Chamando o Solver ##
solver = pyEnv.SolverFactory('glpk', executable = '/usr/bin/glpsol')
result_objetivo = solver.solve(modelo, tee = True)

## Printando o resultado ##
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
