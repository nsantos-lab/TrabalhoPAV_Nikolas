# 4) Crie uma função que receba três valores, 'a', 'b' e 'c', que são os
# coeficientes de uma equação do segundo grau e apresente o valor do
# delta, que é dado por 'b2 - 4ac'.

# Definição/implementação da função
# valores default: pode espeficar parâmetros com valor default
def calcula_delta(a=2, b=2, c=1):
    delta = b**2 - 4*a*c
    return delta

n1 = float(input("Digite o valor do coeficiente 'a':"))
n2 = float(input("Digite o valor do coeficiente 'b':"))
n3 = float(input("Digite o valor do coeficiente 'c':"))

d = calcula_delta(n1, n2, n3)
#OU
d = calcula_delta(c=n3, a=n1, b=n2)
#OU
# execução da função: passando apenas o parâmetro 'a'. Vai pela ordem dos parâmetros
d = calcula_delta(n1) # a = n1, b e c recebem os valores default
# execução da função: passando apenas o parâmetro 'b'. 
d = calcula_delta(b=n2) # b = n2, mas a e c recebem os valores default
# execução da função: passando apenas o parâmetro 'c'. 
d = calcula_delta(c=n3) # c = n3, mas a e b recebem os valores default

print(f"Delta = {d}")
