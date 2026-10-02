# MODELA UM objeto
# Definição de classe em python. class <nomedaclasse>:
class Motor:
    def __init__(self, cilindrada, potencia):
        self.cilindrada = cilindrada
        self.potencia = potencia

class Veiculo:
    # Seguir a identação para definir atributos e métodos da classe
    # Não declara atributos NESSE momento
    # Ex: modelo, placa, cor, ano, marca

    # Criar outro construtor para a classe. Usa o método init
    # self: Representa o objeto. Ex: this
    # "Sobrecarga" de construtor
    def __init__(self, modelo=None, placa=None, cor=None, ano=None, marca=None, motor=None):
        # Definindo e "instanciando" atributos da classe
        # publico
        self.modelo = modelo
        self.placa = placa
        self.cor = cor
        self.motor = motor
        # privado
        self.__ano = ano
        self.__marca = marca

    # Criar os métodos do veículo
    def acelerar(self):
        pass

    def setModelo(self, modelo):
        # Atributo  classe, modelo, recebe o valor do parâmetro modelo.
        self.modelo = modelo # = this.modelo = modelo

    def getMarca(self):
        return self.__marca

    def getAno(self):
        return self.__ano


# Instanciar um objeto veiculo usando o construtor padrão
v = Veiculo(modelo="Uno", marca="Fiat", ano=1990)
print(v.getMarca())
#print(v.__marca) ## ERRO ao tentar acessar um atributo privado
print(v.getAno())
#print(v.__ano) ## ERRO ao tentar acessar um atributo privado
print(v.modelo) # Funciona porque é um atributo público