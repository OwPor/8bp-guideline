import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QTransform

class TransparentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)

class PoolOverlay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.lineStart = QPoint(400, 300)
        self.lineEnd = QPoint(400, 400)
        self.drawing = False

    def initUI(self):
        self.setWindowTitle('8 Ball Pool -Vince')
        self.setGeometry(100, 100, 900, 410)
        self.setWindowOpacity(0.3)
        self.transparent_widget = TransparentWidget(self)
        self.setCentralWidget(self.transparent_widget)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.blue, 20, Qt.SolidLine))
        painter.drawLine(self.lineStart, self.lineEnd)
        painter.setPen(QPen(Qt.red, 16, Qt.SolidLine))
        painter.drawLine(self.lineStart, self.lineEnd)
        painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
        painter.drawLine(self.lineStart, self.lineEnd)

        # Check if the line has hit the edge
        if self.lineEnd.x() in (self.rect().left(), self.rect().right()) or \
        self.lineEnd.y() in (self.rect().top(), self.rect().bottom()):
            # Calculate the mirrored line start and end points
            mirroredLineStart = self.calculateMirroredPoint(self.lineStart)
            
            # Draw the mirrored line
            painter.setPen(QPen(Qt.blue, 20, Qt.SolidLine))
            painter.drawLine(self.lineEnd, mirroredLineStart)
            painter.setPen(QPen(Qt.red, 16, Qt.SolidLine))
            painter.drawLine(self.lineEnd, mirroredLineStart)
            painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
            painter.drawLine(self.lineEnd, mirroredLineStart)


    def calculateMirroredPoint(self, point):
        # Calculate the mirrored point across the X-axis (for Y-axis, swap X and Y)
        mirroredX = self.rect().width() - point.x()  # X-coordinate stays the same
        mirroredY = point.y()  # Y-coordinate is mirrored
        return QPoint(mirroredX, mirroredY)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lineStart = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def mouseMoveEvent(self, event):
        if self.drawing:
            newLineEnd = event.pos()
            newLineEnd.setX(max(self.rect().left(), min(newLineEnd.x(), self.rect().right())))
            newLineEnd.setY(max(self.rect().top(), min(newLineEnd.y(), self.rect().bottom())))
            self.lineEnd = newLineEnd
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PoolOverlay()
    sys.exit(app.exec_())
