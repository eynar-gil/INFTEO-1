# grafo_pyqt5.py
import sys
import time
from PyQt5 import QtWidgets, QtCore, QtGui
import networkx as nx

class AnimadorThread(QtCore.QThread):
    visitar_nodo = QtCore.pyqtSignal(int)
    resaltar_arista = QtCore.pyqtSignal(int, int)
    restaurar_nodo = QtCore.pyqtSignal(int)
    terminar = QtCore.pyqtSignal(float)
    estado_text = QtCore.pyqtSignal(str, QtGui.QColor)

    def __init__(self, recorrido, delay=1.0, parent=None):
        super().__init__(parent)
        self.recorrido = recorrido
        self.delay = delay
        self._running = True

    def run(self):
        start_time = time.time()
        self.estado_text.emit(f"Recorriendo: {self.recorrido}", QtGui.QColor("black"))
        if not self.recorrido:
            self.estado_text.emit("Recorrido vacío.", QtGui.QColor("red"))
            self.terminar.emit(0.0)
            return

        for i in range(len(self.recorrido) - 1):
            if not self._running:
                break
            actual = self.recorrido[i]
            siguiente = self.recorrido[i + 1]
            self.visitar_nodo.emit(actual)
            self.resaltar_arista.emit(actual, siguiente)
            self.estado_text.emit(f"Visitando nodo: {actual} → {siguiente}", QtGui.QColor("black"))
            time.sleep(self.delay)
            self.restaurar_nodo.emit(actual)

        if self._running:
            ultimo = self.recorrido[-1]
            self.visitar_nodo.emit(ultimo)
            self.estado_text.emit(f"Visitando nodo final: {ultimo}", QtGui.QColor("black"))
            time.sleep(self.delay)
            self.restaurar_nodo.emit(ultimo)

        end_time = time.time()
        total = end_time - start_time
        self.estado_text.emit("Recorrido finalizado", QtGui.QColor("green"))
        self.terminar.emit(total)

    def stop(self):
        self._running = False

class NodoItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, x, y, r, label, parent=None):
        super().__init__(-r, -r, 2*r, 2*r, parent)
        self.setPos(x, y)
        self.r = r
        self.label = label
        self.setBrush(QtGui.QBrush(QtGui.QColor("lightgray")))
        self.setPen(QtGui.QPen(QtGui.QColor("black"), 2))
        self.text_item = QtWidgets.QGraphicsTextItem(str(label), self)
        font = QtGui.QFont("Arial", 14, QtGui.QFont.Bold)
        self.text_item.setFont(font)
        rect = self.text_item.boundingRect()
        self.text_item.setPos(-rect.width()/2, -rect.height()/2)

class AristaItem(QtWidgets.QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2, source, target, parent=None):
        super().__init__(x1, y1, x2, y2, parent)
        self.source = source
        self.target = target
        pen = QtGui.QPen(QtGui.QColor("black"), 2)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        self.setPen(pen)

class GrafoApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recorrido de grafo - PyQt5 (0–6)")
        self.resize(720, 560)

        # Grafo
        self.G = nx.DiGraph()
        self.G.add_nodes_from([0,1,2,3,4,5,6])
        self.G.add_edges_from([(2,0),(0,6),(0,5),(6,3),(6,5),(6,4),(1,4),(0,1)])

      
        self.pos = {
            2: (80, 100), 0: (180, 100), 6: (280, 100), 3: (380, 100),
            5: (225, 180), 4: (280, 260), 1: (180, 260)
        }

        layout = QtWidgets.QVBoxLayout(self)

        self.scene = QtWidgets.QGraphicsScene(0, 0, 600, 400)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        layout.addWidget(self.view)

       
        control_layout = QtWidgets.QHBoxLayout()
        control_label = QtWidgets.QLabel("Recorrido (ej. 2, 0, 6, 4, 1):")
        control_layout.addWidget(control_label)
        self.entry = QtWidgets.QLineEdit("2, 0, 6, 4, 1")
        self.entry.setFixedWidth(220)
        control_layout.addWidget(self.entry)
        self.btn_iniciar = QtWidgets.QPushButton("Iniciar recorrido")
        control_layout.addWidget(self.btn_iniciar)
        layout.addLayout(control_layout)

       
        self.lbl_estado = QtWidgets.QLabel("Esperando inicio...")
        self.lbl_estado.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.lbl_estado)
        self.lbl_tiempo = QtWidgets.QLabel("Tiempo recorrido: 0.0 segundos")
        self.lbl_tiempo.setFont(QtGui.QFont("Arial", 10))
        layout.addWidget(self.lbl_tiempo)

        self.node_items = {}
        self.edge_items = {}

        self.dibujar_grafo()

        self.btn_iniciar.clicked.connect(self.on_iniciar)
        self.anim_thread = None

    def dibujar_grafo(self):
       
        for u, v in self.G.edges():
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            line = AristaItem(x1, y1, x2, y2, source=u, target=v)
            self.scene.addItem(line)
            self.edge_items[(u, v)] = line

       
        for n, (x, y) in self.pos.items():
            nodo = NodoItem(x, y, 28, n)
            self.scene.addItem(nodo)
            self.node_items[n] = nodo

    def on_iniciar(self):
        texto = self.entry.text().strip()
        try:
            recorrido = [int(t.strip()) for t in texto.split(",") if t.strip() != ""]
        except ValueError:
            self.set_estado("Error en el formato del recorrido.", QtGui.QColor("red"))
            return

        for n in recorrido:
            if n not in self.G.nodes:
                self.set_estado("Algunos nodos no existen en el grafo.", QtGui.QColor("red"))
                return

        self.btn_iniciar.setEnabled(False)
        if self.anim_thread and self.anim_thread.isRunning():
            self.anim_thread.stop()
            self.anim_thread.wait(200)

        self.anim_thread = AnimadorThread(recorrido, delay=1.0)
        self.anim_thread.visitar_nodo.connect(self.slot_visitar_nodo)
        self.anim_thread.resaltar_arista.connect(self.slot_resaltar_arista)
        self.anim_thread.restaurar_nodo.connect(self.slot_restaurar_nodo)
        self.anim_thread.terminar.connect(self.slot_terminar)
        self.anim_thread.estado_text.connect(self.set_estado)
        self.anim_thread.start()

    @QtCore.pyqtSlot(str, QtGui.QColor)
    def set_estado(self, texto, color=QtGui.QColor("black")):
        if isinstance(color, QtGui.QColor):
            qcolor = color
        else:
            qcolor = QtGui.QColor(str(color))
        self.lbl_estado.setText(texto)
        palette = self.lbl_estado.palette()
        palette.setColor(self.lbl_estado.foregroundRole(), qcolor)
        self.lbl_estado.setPalette(palette)

    @QtCore.pyqtSlot(int)
    def slot_visitar_nodo(self, nodo):
        item = self.node_items.get(nodo)
        if item:
            item.setBrush(QtGui.QBrush(QtGui.QColor("orange")))
            item.text_item.setDefaultTextColor(QtGui.QColor("white"))

    @QtCore.pyqtSlot(int)
    def slot_restaurar_nodo(self, nodo):
        item = self.node_items.get(nodo)
        if item:
            item.setBrush(QtGui.QBrush(QtGui.QColor("lightgray")))
            item.text_item.setDefaultTextColor(QtGui.QColor("black"))

    @QtCore.pyqtSlot(int, int)
    def slot_resaltar_arista(self, n1, n2):
        
        for (u, v), line in self.edge_items.items():
            pen = QtGui.QPen(QtGui.QColor("black"), 2)
            line.setPen(pen)
        
        line = self.edge_items.get((n1, n2))
        if line:
            pen = QtGui.QPen(QtGui.QColor("blue"), 4)
            pen.setCapStyle(QtCore.Qt.RoundCap)
            line.setPen(pen)

    @QtCore.pyqtSlot(float)
    def slot_terminar(self, tiempo_total):
        self.lbl_tiempo.setText(f"Tiempo recorrido: {tiempo_total:.2f} segundos")
        self.btn_iniciar.setEnabled(True)

def main():
    app = QtWidgets.QApplication(sys.argv)
    ventana = GrafoApp()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
