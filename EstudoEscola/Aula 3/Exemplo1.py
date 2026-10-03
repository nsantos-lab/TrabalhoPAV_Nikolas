# Set {}
frutas = {"Laranja", "Uva", "Maçã"}

print(frutas)
print(type(frutas))

# print(frutas[0]) ERRADO. Não é possível acessar um objeto no set pelo índice.
# SET NÃO TEM ÍNDICE

frutas.add("Manga")
# não há ordenação de valores ao apresentar o set
print(frutas)

# Não permite valores repetidos dentro do conjunto. 
frutas.add("Laranja")
print(frutas)

# Conversão de set para lista
list_frutas = list(frutas)
print(list_frutas)

