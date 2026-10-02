# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import json
import requests

from PySide2 import QtWidgets
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class Widget(QtWidgets.QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.load_ui()

        self.btn_cadastrar = self.findChild(QtWidgets.QPushButton, 'btn_cadastrar')
        self.btn_buscar = self.findChild(QtWidgets.QPushButton, 'btn_buscar')
        self.btn_editar = self.findChild(QtWidgets.QPushButton, 'btn_editar')
        self.btn_excluir = self.findChild(QtWidgets.QPushButton, 'btn_excluir')
        self.btn_limpar = self.findChild(QtWidgets.QPushButton, 'btn_limpar')

        self.setupStyle()

        self.btn_cadastrar.clicked.connect(self.callAPIPost)
        self.btn_buscar.clicked.connect(self.callAPIGet)
        self.btn_editar.clicked.connect(self.callAPIPut)
        self.btn_excluir.clicked.connect(self.callAPIDelete)
        self.btn_limpar.clicked.connect(self.limparCampos)

        titulo = self.findChild(QtWidgets.QLabel, 'lbl_titulo')
        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2d3436;
        """)
        lineId = self.findChild(QtWidgets.QLineEdit, 'lineId')
        lineNome = self.findChild(QtWidgets.QLineEdit, 'lineNome')
        lineMatricula = self.findChild(QtWidgets.QLineEdit, 'lineMatricula')

        lineId.setPlaceholderText("Digite o ID do aluno")
        lineNome.setPlaceholderText("Digite o nome")
        lineMatricula.setPlaceholderText("Digite a matrícula")

        lineId.setClearButtonEnabled(True)
        lineNome.setClearButtonEnabled(True)
        lineMatricula.setClearButtonEnabled(True)

        self.center()


    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setupStyle(self):
        self.setWindowTitle("Sistema Acadêmico")
        #self.resize(650, 420)

        self.setStyleSheet("""

        QWidget {
            background-color: #f5f6fa;
            font-family: Segoe UI;
            font-size: 14px;
        }

        QLabel {
            color: #2f3640;
            font-weight: bold;
        }

        QLineEdit {
            background: white;
            border: 2px solid #dcdde1;
            border-radius: 8px;
            padding-left: 10px;
            height: 36px;
        }

        QLineEdit:focus {
            border: 2px solid #3498db;
        }

        QPushButton {
            background-color: #0984e3;
            color: white;
            border: none;
            border-radius: 8px;
            min-height: 40px;
            padding: 0 18px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #74b9ff;
        }

        QPushButton:pressed {
            background-color: #0652DD;
        }

        """)

        self.btn_cadastrar.setStyleSheet("""
        QPushButton {
            background-color: #0984e3;
            color: white;
            border-radius: 8px;
            min-height: 40px;
            font-weight: bold;
        }
        """)

        self.btn_buscar.setStyleSheet("""
        QPushButton {
            background-color: #6c5ce7;
            color: white;
            border-radius: 8px;
            min-height: 40px;
            font-weight: bold;
        }
        """)

        self.btn_editar.setStyleSheet("""
        QPushButton {
            background-color: #e17055;
            color: white;
            border-radius: 8px;
            min-height: 40px;
            font-weight: bold;
        }
        """)

        self.btn_excluir.setStyleSheet("""
        QPushButton {
            background-color: #d63031;
            color: white;
            border-radius: 8px;
            min-height: 40px;
            font-weight: bold;
        }
        """)

        self.btn_limpar.setStyleSheet("""
        QPushButton {
            background-color: #636e72;
            color: white;
            border-radius: 8px;
            min-height: 40px;
            font-weight: bold;
        }
        """)

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def printButtonPressed(self):
        # This is executed when the button is pressed
        print('printButtonPressed')

    def limparCampos(self):
        id = self.findChild(QtWidgets.QLineEdit, 'lineId')
        nome = self.findChild(QtWidgets.QLineEdit, 'lineNome')
        matricula = self.findChild(QtWidgets.QLineEdit, 'lineMatricula')
        id.setText("")
        nome.setText("")
        matricula.setText("")

    def callAPIGet(self):
        alunoId = self.findChild(QtWidgets.QLineEdit, 'lineId')
        if alunoId.text() == "":
            alunoId.setText("É necessário definir o Id a ser buscado.")
        response = requests.get(f"http://localhost:8080/academico/alunos/{alunoId.text()}")
        data = response.json()
        nome = self.findChild(QtWidgets.QLineEdit, 'lineNome')
        matricula = self.findChild(QtWidgets.QLineEdit, 'lineMatricula')
        if nome and 'nome' in data:
            nome.setText(data["nome"])
        if matricula and 'matricula' in data:
            matricula.setText(data["matricula"])

    def callAPIPost(self):
        # Obtém os dados de cada campo da tela
        id = self.findChild(QtWidgets.QLineEdit, 'lineId')
        nome = self.findChild(QtWidgets.QLineEdit, 'lineNome')
        matricula = self.findChild(QtWidgets.QLineEdit, 'lineMatricula')
        # Montando um json com esses valores
        data = {
            "id": int(id.text()),
            "nome": nome.text(),
            "matricula": matricula.text(),
        }
        response = requests.post("http://localhost:8080/academico/alunos", data=data)
        self.limparCampos()
        print(response.json())

    def callAPIPut(self):
        id = self.findChild(QtWidgets.QLineEdit, 'lineId')
        nome = self.findChild(QtWidgets.QLineEdit, 'lineNome')
        matricula = self.findChild(QtWidgets.QLineEdit, 'lineMatricula')
        data = {
            "nome": nome.text(),
            "matricula": matricula.text(),
        }
        response = requests.put(f"http://localhost:8080/academico/alunos/{id.text()}", data=data)
        self.limparCampos()
        print(response.json())

    def callAPIDelete(self):
        alunoId = self.findChild(QtWidgets.QLineEdit, 'lineId')
        requests.delete(f"http://localhost:8080/academico/alunos/{alunoId.text()}")
        self.limparCampos()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
