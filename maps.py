from sys import argv, exit
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import requests
from PyQt5.QtCore import Qt

api_server = "http://static-maps.yandex.ru/1.x/"
map_file = 'map.png'



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('main.ui', self)
        self.cords = '0,0'
        self.zoom = 5
        self.kind = 'map'
        self.depict()
        self.Up.clicked.connect(self.move)
        self.Down.clicked.connect(self.move)
        self.Right.clicked.connect(self.move)
        self.Left.clicked.connect(self.move)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.zoom < 17:
            self.zoom += 1
        if event.key() == Qt.Key_PageDown and self.zoom > 0:
            self.zoom -= 1
        self.depict()

    def depict(self):
        params = {
            "ll": self.cords,
            "z": self.zoom,
            "l": self.kind
        }
        response = requests.get(api_server, params=params)
        if not response:
            print(response.content)
        with open(map_file, mode='wb') as f:
            f.write(response.content)
        pixmap = QPixmap('map.png')
        self.map_label.setPixmap(pixmap)
        self.map_label.resize(self.map_label.sizeHint())

    def move(self):
        x, y = [float(i) for i in self.cords.split(',')]
        shift = 360 / (2 ** self.zoom)
        if self.sender().text() == '^':
            y += shift
            if y + shift/2 >= 90:
                y -= shift
        elif self.sender().text() == 'V':
            y -= shift
            if y - shift/2 <= -90:
                y += shift
        elif self.sender().text() == '<':
            x -= shift
            if x < -180:
                x = 180 - x % 180
        elif self.sender().text() == '>':
            x += shift
            if x > 180:
                x = -180 + x % 180
        self.cords = '{},{}'.format(x, y)
        self.depict()
if __name__ == '__main__':
    app = QApplication(argv)
    ex = Window()
    ex.show()
    exit(app.exec())