# 1) Escrever um programa que permita ao usuário escolher dentre as
# figuras geométricas círculo, retângulo e triângulo para calcular a área da
# figura escolhida. Implemente o cálculo de área de cada figura e para um
# menu de escolha.

opcao = 0
# : = { -> Abertura de um bloco de código. 
# Identação dita em qual bloco o código está.
# Tamanho da identação: mínimo 1 espaço. padrão: 1 tab ou 4 espaços.
# os demais comandos do bloco tem que seguir a identação do primeiro comando do bloco
while opcao != 4 : # Não precisa de parêntesis nas condições
    print("1 - Triângulo")
    print("2 - Círculo")
    print("3 - Retângulo")
    print("4 - SAIR")

    # INPUT = SCANF. Permite colocar uma mensagem para o usuário. O valor digitado
    # é atribúido a variável opcao. Retorna uma string e transforma para int.
    opcao = int(input("Digite uma opção:"))

    # switch case
    match opcao:
        case 1:
            base = float(input("Digite a base do triângulo:"))
            alt = float(input("Digite a altura do triângulo:"))
            area = base * alt / 2
            print(f"Area do triângulo: {area}")
        case 2:
            raio = float(input("Digite o raio do circulo:"))
            area = 3.14 * raio**2 # pow(raio, 2)
            print(f"Area do círculo: {area}")
        case 3:
            base = float(input("Digite a base do retângulo:"))
            alt = float(input("Digite a altura do retângulo:"))
            area = base * alt
            print(f"Area do retângulo: {area}")
        case 4:
            print("Término do programa.")
        case _: # default
            print("Valor inválido")

# Termina o bloco quando a identação "volta" para o ponto anterior
print("Final")