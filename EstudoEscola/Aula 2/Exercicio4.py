# 4) Crie um programa que receba três valores, 'a', 'b' e 'c', que são os
# coeficientes de uma equação do segundo grau e apresente o valor do
# delta, que é dado por 'b2 - 4ac'.

#a = float(input("Digite o valor do coeficiente 'a'"))
#b = float(input("Digite o valor do coeficiente 'b'"))
#c = float(input("Digite o valor do coeficiente 'c'"))
#OU
a, b, c = float(input("Digite o valor do coeficiente 'a'")), float(input("Digite o valor do coeficiente 'b'")), float(input("Digite o valor do coeficiente 'c'"))

delta = b**2 - 4*a*c

print(f"Delta = {delta}")