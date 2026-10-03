# MODELA UM objeto
# Definição de classe em python. class <nomedaclasse>:
class Veiculo:
    # Seguir a identação para definir atributos e métodos da classe
    # Não declara atributos NESSE momento
    # Ex: modelo, placa, cor, ano, marca

    # Criar outro construtor para a classe. Usa o método init
    # self: Representa o objeto. Ex: this
    # "Sobrecarga" de construtor
    def __init__(self, modelo=None, placa=None, cor=None, ano=None, marca=None):
        # Definindo e "instanciando" atributos da classe
        self.modelo = modelo
        self.placa = placa
        self.cor = cor
        self.ano = ano
        self.marca = marca

    # Criar os métodos do veículo
    def acelerar(self):
        pass

    def setModelo(self, modelo):
        # Atributo  classe, modelo, recebe o valor do parâmetro modelo.
        self.modelo = modelo # = this.modelo = modelo


# Instanciar um objeto veiculo usando o construtor padrão
v = Veiculo()
print(v.modelo)
print(type(v))

v1 = Veiculo("Chevette", "RTE-3W34", "Branco", 1989, "Chevrolet")
print(v1.modelo)
print(type(v1))

v2 = Veiculo(marca="Ford")
print(v2.modelo, v2.marca)
print(type(v2))