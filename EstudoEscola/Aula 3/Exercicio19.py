# 19) Faça um programa que receba a temperatura média de cada mês do ano e
# armazene-as em um lista. O programa deverá calcular e mostrar a maior e a menor
# temperatura do ano, juntamente com o mês em que elas ocorreram (o mês deverá ser
# mostrado por extenso: 1 = janeiro; 2 = fevereiro; ...).
# OBSERVAÇÃO: Não se preocupe com empates

# Variável de DOMÍNIO
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

temperaturas = []

for i in range(12):
    temperaturas.append(float(input(f"Digite a temperatura do mês de {meses[i]}:")))
    #OU
    #temperaturas[i] = float(input(f"Digite a temperatura do mês de {meses[i]}:"))
    #OU
    #temperaturas.insert(i, float(input(f"Digite a temperatura do mês de {meses[i]}:")))

maior = temperaturas[0]
menor = temperaturas[0]
indiceMaior = 0
indiceMenor = 0

for i in range(1, 12):
    if temperaturas[i] < menor:
        menor = temperaturas[i]
        indiceMenor = i
    if temperaturas[i] > maior:
        maior = temperaturas[i]
        indiceMaior = i

print(f"Mês de maior temperatura: {meses[indiceMaior]} com temperatura = {maior}")
print(f"Mês de menor temperatura: {meses[indiceMenor]} com temperatura = {menor}")



