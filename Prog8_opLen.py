import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib_venn import venn2


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operaciones entre Lenguajes - Diagrama de Venn")
        self.setGeometry(100, 100, 800, 600)

        layout_principal = QVBoxLayout()

        layout_inputs = QHBoxLayout()
        self.input_L1 = QLineEdit()
        self.input_L1.setPlaceholderText("Ejemplo: aa, ab, bb, ba")

        self.input_L2 = QLineEdit()
        self.input_L2.setPlaceholderText("Ejemplo: ab, ba, cc")

        layout_inputs.addWidget(QLabel("Lenguaje L1:"))
        layout_inputs.addWidget(self.input_L1)
        layout_inputs.addWidget(QLabel("Lenguaje L2:"))
        layout_inputs.addWidget(self.input_L2)
        layout_principal.addLayout(layout_inputs)

        layout_botones = QHBoxLayout()
        self.btn_union = QPushButton("Unión (∪)")
        self.btn_inter = QPushButton("Intersección (∩)")
        self.btn_dif = QPushButton("Diferencia (−)")
        self.btn_complemento = QPushButton("Complementos")

        layout_botones.addWidget(self.btn_union)
        layout_botones.addWidget(self.btn_inter)
        layout_botones.addWidget(self.btn_dif)
        layout_botones.addWidget(self.btn_complemento)
        layout_principal.addLayout(layout_botones)

        self.figura = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figura)
        layout_principal.addWidget(self.canvas)

        self.btn_union.clicked.connect(self.mostrar_union)
        self.btn_inter.clicked.connect(self.mostrar_inter)
        self.btn_dif.clicked.connect(self.mostrar_diferencia)
        self.btn_complemento.clicked.connect(self.mostrar_complementos)

        self.setLayout(layout_principal)

    def obtener_lenguajes(self):
        L1_texto = self.input_L1.text().strip()
        L2_texto = self.input_L2.text().strip()

        if not L1_texto or not L2_texto:
            QMessageBox.warning(self, "Error", "Debes ingresar ambos lenguajes.")
            return None, None

        L1 = set(x.strip() for x in L1_texto.split(",") if x.strip())
        L2 = set(x.strip() for x in L2_texto.split(",") if x.strip())

        return L1, L2

    def mostrar_union(self):
        L1, L2 = self.obtener_lenguajes()
        if L1 is None:
            return
        resultado = L1.union(L2)
        self.graficar(L1, L2, f"Unión (L1 ∪ L2): {resultado}")

    def mostrar_inter(self):
        L1, L2 = self.obtener_lenguajes()
        if L1 is None:
            return
        resultado = L1.intersection(L2)
        self.graficar(L1, L2, f"Intersección (L1 ∩ L2): {resultado}")

    def mostrar_diferencia(self):
        L1, L2 = self.obtener_lenguajes()
        if L1 is None:
            return
        resultado = L1.difference(L2)
        self.graficar(L1, L2, f"Diferencia (L1 − L2): {resultado}")

    def mostrar_complementos(self):
        L1, L2 = self.obtener_lenguajes()
        if L1 is None:
            return
        U = L1.union(L2)
        complemento_L1 = U.difference(L1)
        complemento_L2 = U.difference(L2)
        mensaje = f"Complemento de L1: {complemento_L1}\nComplemento de L2: {complemento_L2}"
        QMessageBox.information(self, "Complementos", mensaje)
        self.graficar(L1, L2, "Complementos mostrados en mensaje")
        
    def graficar(self, L1, L2, titulo):
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        venn2([L1, L2], set_labels=("L1", "L2"), ax=ax)
        ax.set_title(titulo, fontsize=11)
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())