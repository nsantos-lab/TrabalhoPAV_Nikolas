# 4) Crie uma função que receba três valores, 'a', 'b' e 'c', que são os
# coeficientes de uma equação do segundo grau e apresente o valor do
# delta, que é dado por 'b2 - 4ac'.

# Definição/implementação da função
# Pode dar uma "dica" dos tipos dos parâmetros e do retorno
# Ao inserir os tipos esperados estamos aumentando a qualidade do código
def calcula_delta(a: float, b: float, c: float) -> float:
    delta = b**2 - 4*a*c
    return delta

n1 = float(input("Digite o valor do coeficiente 'a':"))
n2 = float(input("Digite o valor do coeficiente 'b':"))
n3 = float(input("Digite o valor do coeficiente 'c':"))

d = calcula_delta(n1, n2, n3)

print(f"Delta = {d}")
