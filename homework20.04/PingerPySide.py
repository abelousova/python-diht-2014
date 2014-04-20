import sys
from PySide.QtCore import *
from PySide.QtGui import *
import threading
import subprocess
import queue
import logging
import argparse


app = QApplication(sys.argv)


class PingerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(300, 400))
        self.setWindowTitle('Pinger')
        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        self.textbox = IPTextBox(self)
        self.button = CheckIPButton(self)
        self.results = ResultsTextBox(self)
        self.label = ResultLabel(self)

        self.form_layout.addRow('IP:', self.textbox)
        self.form_layout.addRow(self.button)
        self.form_layout.addRow(self.results)

        self.layout.addLayout(self.form_layout)
        self.setLayout(self.layout)

        self.num_threads = 4
        self.taskQueue = queue.Queue()

    def run(self):
        for i in range(self.num_threads):
            t = threading.Thread(target=self.pinger, args=('testFile.txt',))
            t.setDaemon(True)
            t.start()

        self.show()
        app.exec_()
        self.taskQueue.join()

    @Slot()
    def clicked_slot(self):
        self.taskQueue.put(self.textbox.text())

    def pinger(self, fileName):
        logger = logging.getLogger('logName')
        if not logger.hasHandlers():
            hdlr = logging.FileHandler(fileName)
            hdlr.setFormatter(logging.Formatter('%(message)s'))
            logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)
        while True:
            ip = self.taskQueue.get()
            with open('NUL', 'w') as f:
                returnValue = subprocess.call('ping {0}'.format(ip), stdout=f, stderr=f)
            if returnValue == 0:
                logger.info(ip)
                self.results.insertPlainText('good ip: {0}\n'.format(ip))
            else:
                self.results.insertPlainText('bad ip: {0}\n'.format(ip))
            self.taskQueue.task_done()


class Press(QKeyEvent):
    def __init__(self):
        super().__init__()
        print('Button')


class CheckIPButton(QPushButton):
    def __init__(self, widget):
        super().__init__('Check IP', widget)
        self.clicked.connect(widget.clicked_slot)


class IPTextBox(QLineEdit):
    def __init__(self, widget):
        super().__init__('print IP..', widget)


class ResultsTextBox(QTextEdit):
    def __init__(self, widget):
        QTextEdit.__init__(self, '', widget)
        self.setReadOnly(True)


class ResultLabel(QLabel):
    def __init__(self, widget):
        QLabel.__init__(self, widget)



PingerApp().run()