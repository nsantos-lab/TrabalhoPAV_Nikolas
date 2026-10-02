# 19) Faça um programa que receba a temperatura média de cada mês do ano e
# armazene-as em um lista. O programa deverá calcular e mostrar a maior e a menor
# temperatura do ano, juntamente com o mês em que elas ocorreram (o mês deverá ser
# mostrado por extenso: 1 = janeiro; 2 = fevereiro; ...).
# OBSERVAÇÃO: Não se preocupe com empates

def lerTemperaturas(meses):
    temperaturas = []
    for i in range(12):
        temperaturas.append(float(input(f"Digite a temperatura do mês de {meses[i]}:")))
    return temperaturas

# O ideal é que cada função tenha apenas UMA "tarefa" específica
# Facilita a reutilização
def calcularMaiorMenor(temperaturas):
    # Encontrar o índice dessa temperatura na lista
    indiceMaior = temperaturas.index(max(temperaturas))
    indiceMenor = temperaturas.index(min(temperaturas))
    return indiceMaior, indiceMenor

def mostrarMaiorMenor(indiceMaior, indiceMenor, meses, temperaturas):
    print(f"Mês de maior temperatura: {meses[indiceMaior]} com temperatura = {temperaturas[indiceMaior]}")
    print(f"Mês de menor temperatura: {meses[indiceMenor]} com temperatura = {temperaturas[indiceMenor]}")

# Variável de DOMÍNIO
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

temperaturas = lerTemperaturas(meses)
indexMaior, indexMenor = calcularMaiorMenor(temperaturas)
mostrarMaiorMenor(indexMaior, indexMenor, meses, temperaturas)
