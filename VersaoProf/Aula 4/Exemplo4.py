# MODELA UM objeto
# Definição de classe em python. class <nomedaclasse>:
class Veiculo:
    # Seguir a identação para definir atributos e métodos da classe
    # Não declara atributos NESSE momento
    # Ex: modelo, placa, cor, ano, marca

    # Criar outro construtor para a classe. Usa o método init
    # self: Representa o objeto. Ex: this
    # "Sobrecarga" de construtor
    def __init__(self):
        # Definindo e "instanciando" atributos da classe
        # privado
        self.__modelo = None
        self.__placa = None
        self.__cor = None
        self.__ano = None
        self.__marca = None

    # Criar os métodos do veículo
    def acelerar(self):
        pass

    def setModelo(self, modelo):
        # Atributo  classe, modelo, recebe o valor do parâmetro modelo.
        self.__modelo = modelo # = this.modelo = modelo

    def getModelo(self):
        return self.__modelo

    def setMarca(self, marca):
        self.__marca = marca

    def getMarca(self):
        return self.__marca

    def setAno(self, ano):
        self.__ano = ano

    def getAno(self):
        return self.__ano


# Instanciar um objeto veiculo usando o construtor padrão
v = Veiculo()
v.setModelo("Gol")
v.setAno(1998)
v.setMarca("VW")
print(v.getModelo())
