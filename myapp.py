import sys
from PyQt5.QtWidgets import *
import demo as ya

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.lbl1 = QLabel('링크:', self)
        self.lbl2 = QLabel('', self)
        self.le = QLineEdit(self)
        self.trans_btn = QPushButton('ADD', self)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl1)
        vbox.addWidget(self.le)
        vbox.addWidget(self.trans_btn)
        vbox.addWidget(self.lbl2)
        self.setLayout(vbox)

        self.trans_btn.clicked.connect(self.translate)
        # self.le.editingFinished.connect(self.translate_kor)

        self.setWindowTitle('Video Information')
        self.setGeometry(300, 300, 400, 200)
        self.show()

    def translate(self):
        link = self.le.text()
        print(link)
        id = ya.video_id(link)
        text = ya.video2excel(id)
        self.lbl2.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())