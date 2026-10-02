# tuple ()

funcionario = ('joão', '15/08/2006', 3500.00)
print(funcionario)
print(type(funcionario))

# Não é posssível adicionar/remover valores: não tem add, insert, append, remove, pop
# IMUTÁVEL
# Pode iterar, possui índice e ordem.
print(funcionario[0])
print(funcionario.index(3500.00))

# Muito usado para armazenar dados vindos do BD
