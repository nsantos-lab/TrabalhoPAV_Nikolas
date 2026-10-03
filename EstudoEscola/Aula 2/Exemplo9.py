# VETOR EM PYTHON: não existe com esse nome
# Python tem: list, set, tuple, dict

# list
# Não precisa de definir tamanho.
lista_de_frutas = ["LARANJA", "MAÇÃ"]
# Apresentar um objeto em um índice
print(lista_de_frutas[0])
# Apresentando a lista
print(lista_de_frutas)
# Apresentando o tipo da variável
print(type(lista_de_frutas))

# ADICIONANDO ao final da lista
lista_de_frutas.append("UVA")
print(lista_de_frutas)

# Lista possui índice (igual vetor). NÃO Substitui o valor existente
lista_de_frutas.insert(0, "MANGA")
print(lista_de_frutas)

lista_de_frutas.remove("MAÇÃ")
print(lista_de_frutas)

lista_de_frutas.pop()
print(lista_de_frutas)

lista_de_frutas.pop(0)
print(lista_de_frutas)
#lista = lista_de_frutas.sort("")
#print(lista)
