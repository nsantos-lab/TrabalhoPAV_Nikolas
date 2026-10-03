# Elabore um programa que leia 5 valores reais e
# calcule a média aritmética desses valores.

# 0 ... 4(inclusive) de 1 em 1

soma = 0
# start: 0 (default), stop: 5 (especificado), step: 1 (default)
for i in range(5): #for(int i = 0; i <  5; i++)
    valor = float(input("Digite um valor: "))
    soma += valor

print(f"Média: {soma/5}")

# Soluções análogas ao for anterior
# start: 5, stop: 10, step: 1 (default)
for i in range(5,10): 
    valor = float(input("Digite um valor: "))
    soma += valor

# start: 50, stop: 100, step: 10 
for i in range(50, 100, 10): 
    valor = float(input("Digite um valor: "))
    soma += valor

# start: 5, stop: 0 (ex:5 ... 1 inclusive), step: -1 
for i in range(5, 0, -1): 
    valor = float(input("Digite um valor: "))
    soma += valor
