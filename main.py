import requests
import numpy as np
import base64
import sys
from cv2 import cv2
from datamodel import TrackingOrder
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def get_captcha_challenge():
    try:
        get_captcha = requests.get('https://api.viettelpost.vn/api/orders/getCaptcha').json()
        if get_captcha.get('status') != 200 or get_captcha.get('data') is None:
            return None

        data = get_captcha.get('data')
        if data.get('id') is None or data.get('captcha') is None:
            return None
        else:
            encoded_png = data.get('captcha').split(',')[1]
            img_bytes = np.frombuffer(base64.b64decode(encoded_png), np.uint8)
            img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
            return data.get('id'), img

    except (Exception,) as e:
        print(e)
        return None


def get_tracking_info(captcha_id: str, captcha_answer: str, tracking_number: str):
    try:
        request_data = {
            'captcha': captcha_answer,
            'id': captcha_id,
            'orders': tracking_number
        }
        server_response = requests.post('https://api.viettelpost.vn/api/orders/viewTrackingOrders',
                                        json=request_data).json()
        if server_response.get('status') != 200 or server_response.get('data') is None:
            return None

        datas = server_response.get('data')
        orders = [TrackingOrder(i) for i in datas]
        return orders
    except (Exception,) as e:
        print(e)
        return None


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Viettelpost tracking')
        self.captcha_id = None
        self.image = QImage(np.full((50, 200, 3), 0, np.uint8).data, 200, 50, QImage.Format_RGB888)
        self.image_frame = QLabel()
        self.image_frame.setPixmap(QPixmap.fromImage(self.image))
        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        self.order_box = QLineEdit()

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel('Enter tracking order number (e.g.: 123,456,789,...):'))
        self.layout.addWidget(self.order_box)

        self.layout.addWidget(QLabel('Enter captcha:'))
        self.layout.addWidget(self.image_frame)
        self.captcha_box = QLineEdit()
        self.layout.addWidget(self.captcha_box)

        self.enter_button = QPushButton('Submit')
        self.enter_button.clicked.connect(self.enter_captcha)
        self.layout.addWidget(self.enter_button)
        self.reload_captcha_button = QPushButton('Reload captcha')
        self.reload_captcha_button.clicked.connect(self.reload_captcha)
        self.layout.addWidget(self.reload_captcha_button)
        self.layout.addWidget(self.output_console)

        self.reload_captcha()

        self.setLayout(self.layout)

    @pyqtSlot()
    def reload_captcha(self):
        self.captcha_id, self.image = get_captcha_challenge()
        if self.image is not None:
            self.image = QImage(self.image.data, 200, 50, QImage.Format_RGB888)
            self.image_frame.setPixmap(QPixmap.fromImage(self.image))
        else:
            self.output_console.setText('Error when reloading captcha.')

    @pyqtSlot()
    def enter_captcha(self):
        captcha_answer = self.captcha_box.text()
        order_number = self.order_box.text()

        if captcha_answer == '':
            self.output_console.setText('Captcha is empty.')
        elif order_number == '':
            self.output_console.setText('Tracking number is empty.')
        else:
            orders = get_tracking_info(self.captcha_id, captcha_answer, order_number)
            if orders is None:
                self.output_console.setText('An error occurred.')
            else:
                output = ''
                for order in orders:
                    output += str(order) + '-----------------------------------------\n'
                self.output_console.setText(output)
            self.reload_captcha()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.setMinimumWidth(500)
    window.show()
    sys.exit(app.exec_())
