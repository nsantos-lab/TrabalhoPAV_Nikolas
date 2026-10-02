# dict ou dicionário = json
# propriedades: key, value
funcionario = {"nome": "João", "Data de Nascimento": "15/08/2006", "Salário": 3500}

print(funcionario)
#print(funcionario[0]) # não funcciona porque não tem KEY = 0
print(funcionario["nome"])

# Adicionando novas propriedades 
funcionario["telefone"] = '24999776655'
print(funcionario)

funcionario["nome"] = 'José'
print(funcionario)

print(funcionario.values())
print(list(funcionario.values()))

print(funcionario.keys())

funcionario["Dependentes"] = [{"nome": "Antonio", "Data de nascimento": "28/07/2025"},
                              {"nome": "Maria", "Data de nascimento": "28/07/2023"}]

funcionario["Função"] = {"cargo": "diretor", "data de início": "27/08/2026"}
print(funcionario)

# Mostrando a função/cargo do funcionário
print(funcionario["Função"]["cargo"])

#Mostrar o primeiro dependente
print(funcionario["Dependentes"][0])

#Mostrar o nome do primeiro dependente
print(funcionario["Dependentes"][0]["nome"])

print(funcionario["Dependentes"][0].keys())
