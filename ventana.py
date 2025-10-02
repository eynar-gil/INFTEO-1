import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt6.QtCore import Qt

class Calculadora(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora PyQt6")
        self.setFixedSize(300, 400)

        # Campo de texto
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)

        # Layout de botones
        grid_layout = QGridLayout()
        botones = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
            ("0", 3, 0), (".", 3, 1), ("=", 3, 2), ("+", 3, 3),
        ]

        for texto, fila, col in botones:
            boton = QPushButton(texto)
            boton.setFixedSize(60, 60)
            # Conecta cada botón a la función correcta
            boton.clicked.connect(lambda checked, t=texto: self.on_button_click(t))
            grid_layout.addWidget(boton, fila, col)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def on_button_click(self, texto):
        if texto == "=":
            try:
                # Evalúa la operación
                resultado = str(eval(self.display.text()))
                self.display.setText(resultado)
            except Exception:
                self.display.setText("Error")
        else:
            self.display.setText(self.display.text() + texto)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculadora()
    calc.show()
    sys.exit(app.exec())
    


