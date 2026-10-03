# MODELA UM objeto
# Definição de classe em python. class <nomedaclasse>:
class Veiculo:
    def __init__(self, modelo: str=None, placa: str=None, cor: str=None, ano: int=None, marca: str=None):
        self.__modelo = modelo
        self.__placa = placa
        self.__cor = cor
        self.__ano = ano
        self.__marca = marca

    # Criar os métodos do veículo
    def acelerar(self):
        print("Acelera veículo")

    def setModelo(self, modelo: str):
        self.__modelo = modelo 

    def getModelo(self):
        return self.__modelo

    def setMarca(self, marca: str):
        self.__marca = marca

    def getMarca(self):
        return self.__marca

    def setAno(self, ano: int):
        self.__ano = ano

    def getAno(self):
        return self.__ano

# Herança. class nomedaclasse(classequeherda)
class Carro(Veiculo): # Carro herda de veiculo
    def __init__(self, modelo: str=None, placa: str=None, cor: str=None, ano: int=None, marca: str=None, tamPortaMala: int=None, numLugares: int=None):
        # Construtor da classe "mãe". Veiculo
        super().__init__(modelo, placa, cor, ano, marca)
        self.__tamPortaMala = tamPortaMala
        self.__numLugares = numLugares

    def getTamPortaMala(self):
        return self.__tamPortaMala

    def getNumLugares(self):
        return self.__numLugares

    # polimorfismo
    def acelerar(self):
        print("Acelera carro")

# Instanciar um objeto carro usando o construtor padrão
c = Carro(modelo="Corolla", tamPortaMala=500)
print(f"Modelo: {c.getModelo()}")
print(f"Tamanho do porta mala: {c.getTamPortaMala()}")
c.acelerar()

c1 = Carro(modelo=500, tamPortaMala=50)
print(f"Modelo: {c1.getModelo()}")
print(f"Tamanho do porta mala: {c1.getTamPortaMala()}")
c1.acelerar()
