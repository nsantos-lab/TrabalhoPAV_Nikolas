#2) Crie um programa que receba um valor e informe se ele é positivo, 
# negativo ou ZERO

valor = float(input("Digite um valor:"))

# Condição simples: if
# Condição composta: if/else
# Condição aninhada: if/else if/ else if.../else
if valor > 0:
    print("Positivo")
elif valor < 0: # em C: else if (valor < 0)
    print("Negativo")
else:
    print("ZERO")
    