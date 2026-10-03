# 4) Crie uma função que receba três valores, 'a', 'b' e 'c', que são os
# coeficientes de uma equação do segundo grau e apresente o valor do
# delta, que é dado por 'b2 - 4ac'.

# Definição/implementação da função
# nome da função (padrão da função) -> parâmetros a, b e c e com retorno
# não precisa especificar o tipo
def calcula_delta(a, b, c):
    delta = b**2 - 4*a*c
    return delta

a = float(input("Digite o valor do coeficiente 'a':"))
b = float(input("Digite o valor do coeficiente 'b':"))
c = float(input("Digite o valor do coeficiente 'c':"))

# execução da função
d = calcula_delta(a, b, c)

print(f"Delta = {d}")
