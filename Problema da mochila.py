## Modelo matemático ##
## Máx 15x1 + 65x2 + 98x3 + 35x4 + 45x5 + 47x6 + 21X7 + 26x8 + 37x9 + 18x10 ##
## S.a 17x1 + 55x2 + 61x3 + 37x4 + 77x5 + 41x6 + 22x7 + 26x8 + 34x9 + 10x10 <= 190 ##

## Caso a implementação esteja sendo feita por uma IDE: ##
## Abra o Anaconda Prompt e insira as seguintes chamadas: ##
## conda install -c conda-forge pyomo ##
## conda install -c conda-forge glpk ##
## Após isto desconsidere os comandos das linhas 12 e 13 ##

## Instalação do pyomo e do solver para o colab ##
!pip install -q pyomo
!apt-get install -y -qq glpk-utils

## Importando a biblioteca pyomo ##
import pyomo.environ as pyEnv

## Dados do problema ##
lucros = [15, 65, 98, 35, 45, 47, 21, 26, 37, 18]
pesos = [17, 55, 61, 37, 77, 41, 22, 26, 34, 10]
capacidade = 190
m = len(lucros)

## Declarando o modelo através da biblioteca ##
modelo = pyEnv.ConcreteModel()

## Criando Indices ##
modelo.Indices = range(m)

## Criando as variáveis ##
modelo.Variaveis = pyEnv.Var(modelo.Indices, within = pyEnv.Binary)

## Criando a Função Objetivo ##
modelo.Objetivo = pyEnv.Objective(expr = sum(lucros[i]*modelo.Variaveis[i] for i in modelo.Indices), sense = pyEnv.maximize)

## Criando as restrições ##
modelo.Restricoes = pyEnv.Constraint(expr = sum(pesos[i]*modelo.Variaveis[i] for i in modelo.Indices) <= capacidade)

## Chamando o Solver ##
solver = pyEnv.SolverFactory('glpk', executable = '/usr/bin/glpsol')
result_objetivo = solver.solve(modelo, tee = True)

## Printando o resultado ##
lista = list(modelo.Variaveis.keys())
print()
print()
print('Variaveis: ')
print()
for i in lista:
  print(i, '---', modelo.Variaveis[i]())
print()
print('Valor da função objetivo =', modelo.Objetivo())
