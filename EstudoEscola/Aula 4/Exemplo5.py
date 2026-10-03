# MODELA UM objeto
# Definição de classe em python. class <nomedaclasse>:
class Veiculo:
    def __init__(self):
        self.__modelo = None
        self.__placa = None
        self.__cor = None
        self.__ano = None
        self.__marca = None

    # Criar os métodos do veículo
    def acelerar(self):
        pass

    def setModelo(self, modelo):
        self.__modelo = modelo 

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

# Herança. class nomedaclasse(classequeherda)
class Carro(Veiculo): # Carro herda de veiculo
    def __init__(self):
        # Construtor da classe "mãe". Veiculo
        super().__init__()
        self.tamPortaMala = None
        self.numLugares = None

# Instanciar um objeto carro usando o construtor padrão
c = Carro()
print(f"Modelo: {c.getModelo()}")
