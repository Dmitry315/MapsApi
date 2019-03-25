from sys import argv, exit
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import requests
from PyQt5.QtCore import Qt

api_server = "http://static-maps.yandex.ru/1.x/"
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
search_api_server = "https://search-maps.yandex.ru/v1/"
map_file = 'map.png'
API_KEY = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('main.ui', self)
        self.cords = '0,0'
        self.zoom = 5
        self.kind = 'map'
        self.map_file = 'map.png'
        self.marks = []
        self.depict()
        self.Up.clicked.connect(self.move)
        self.Down.clicked.connect(self.move)
        self.Right.clicked.connect(self.move)
        self.Left.clicked.connect(self.move)
        self.scheme.clicked.connect(self.change_kind)
        self.satlate.clicked.connect(self.change_kind)
        self.hybrid.clicked.connect(self.change_kind)
        self.search_button.clicked.connect(self.find)
        self.delete_marks_button.clicked.connect(self.delete_marks)
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
            "l": self.kind,
        }
        if self.marks:
            params['pt'] = '~'.join(self.marks)
        response = requests.get(api_server, params=params)
        if not response:
            print(response.content)
        with open(self.map_file, mode='wb') as f:
            f.write(response.content)
        pixmap = QPixmap(self.map_file)
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

    def change_kind(self):
        kind = self.sender().text()
        if kind == 'Схема':
            self.map_file = 'map.png'
            self.kind = 'map'
        elif kind == 'Спутник':
            self.map_file = 'map.jpg'
            self.kind = 'sat'
        elif kind == 'Гибрид':
            self.map_file = 'map.jpg'
            self.kind = 'sat,skl'
        self.depict()

    def find(self):
        try:
            toponym_to_find = self.toponym.text()
            search_params = {
                "apikey": API_KEY,
                "text": toponym_to_find,
                "lang": "ru_RU",
                "type": "geo"
            }
            response = requests.get(search_api_server, params=search_params)
            json_response = response.json()
            organization = json_response["features"][0]
            point = organization["geometry"]["coordinates"]
            geo_point = "{0},{1}".format(point[0], point[1])
            num = str(len(self.marks) + 1)
            mark = geo_point+',pm2rdm' + num
            self.cords = geo_point
            if mark[:-1] not in [i[:-1] for i in self.marks]:
                self.marks.append(mark)
            self.depict()
        except Exception as err:
            pass

    def delete_marks(self):
        self.marks = []
        self.depict()
if __name__ == '__main__':
    app = QApplication(argv)
    ex = Window()
    ex.show()
    exit(app.exec())