import sys
from itertools import product
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QListWidget, QMessageBox, QComboBox
)

class VentanaOperadores(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operadores Regulares sobre Lenguajes")
        self.setGeometry(100, 100, 600, 500)

        layout_principal = QVBoxLayout()

        layout_input = QHBoxLayout()
        layout_input.addWidget(QLabel("Lenguaje base:"))
        self.input_lenguaje = QLineEdit()
        self.input_lenguaje.setPlaceholderText("Ejemplo: a, b, ab, bb")
        layout_input.addWidget(self.input_lenguaje)
        layout_principal.addLayout(layout_input)

        layout_op = QHBoxLayout()
        layout_op.addWidget(QLabel("Operador regular:"))
        self.combo_operador = QComboBox()
        self.combo_operador.addItems(["*", "+", "?"])
        layout_op.addWidget(self.combo_operador)

        self.btn_aplicar = QPushButton("Aplicar operador")
        layout_op.addWidget(self.btn_aplicar)
        layout_principal.addLayout(layout_op)

        layout_principal.addWidget(QLabel("Lenguaje resultante:"))
        self.lista_resultados = QListWidget()
        layout_principal.addWidget(self.lista_resultados)

        self.btn_aplicar.clicked.connect(self.aplicar_operador)

        self.setLayout(layout_principal)

    def obtener_lenguaje(self):
        texto = self.input_lenguaje.text().strip()
        if not texto:
            QMessageBox.warning(self, "Error", "Debes ingresar un conjunto base de cadenas.")
            return None
        return [x.strip() for x in texto.split(",") if x.strip()]

    def aplicar_operador(self):
        base = self.obtener_lenguaje()
        if base is None:
            return

        operador = self.combo_operador.currentText()
        resultado = set()

        if operador == "*":
            resultado.add(" ")
            for i in range(1, 4):  
                for prod in product(base, repeat=i):
                    resultado.add("".join(prod))

        elif operador == "+":
            for i in range(1, 4):
                for prod in product(base, repeat=i):
                    resultado.add("".join(prod))

        elif operador == "?":
            resultado.add(" ")
            resultado.update(base)

        self.mostrar_resultados(resultado, operador)

    def mostrar_resultados(self, resultado, operador):
        self.lista_resultados.clear()
        self.lista_resultados.addItem(f"Operador aplicado: {operador}")
        self.lista_resultados.addItem("Resultados generados:")
        for elem in sorted(resultado):
            self.lista_resultados.addItem(f"  {elem}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaOperadores()
    ventana.show()
    sys.exit(app.exec_())