# Variáveis: 

# Exemplo C: Criar a variável x e atribuir o valor 10 e mostrar o conteúdo de x
# #include <stdio.h>
# int main(){
#    int x;  // definindo uma variável do tipo int
#    x = 10; // atribuindo valor a variável
#    x = 20.5; // ERRO na COMPILAÇÃO 
#    int a; a = 5; printf("A = %d\n", a); // Permite vários comandos em uma linha
#    printf("X = %d\n", x); // apresentando o conteúdo da variável
#}

#Exemplo em Python
# int x -> NÃO EXISTE EM PYTHON
x = 10   # Define e atribui o valor ao mesmo tempo. Infere o tipo da variável de acordo com o valor
#print("X =", x) OU
# String formatada
print(f"X {x}")

# Linguagem TIPADA. Função type: extrai o tipo da variável
# print("Tipo de X = ", type(x)) OU
print(f"Tipo de X = {type(x)}")

x = 20.5
print("Novo valor de X =", x)
print("Novo Tipo de X = ", type(x))

#x = 'PAV' # COM ASPAS SIMPLES OU ASPAS DUPLAS
x = "PAV"
print("Novo valor de X =", x)
print("Novo Tipo de X = ", type(x))

x = True
print(f"Novo X {x}")
print(f"Novo Tipo de X = {type(x)}")

# NÃO permite vários comando na mesma linha 
# x = 5 print(x)

# É Case-sensitive
# nomenclatura de variáveis, objetos, funções, etc segue a mesma regra do C, JAVA, C++