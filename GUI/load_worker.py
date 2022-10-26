from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import time


class LoadWorker(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self, canvas):
        super().__init__()
        self.label_path = ""
        self.canvas = canvas

    def run(self):
        self.load_label()

    def load_path(self, label_path):
        self.label_path = label_path

    def load_label(self):
        if self.label_path:
            with open(self.label_path, "r") as f:
                count = len(open(self.label_path, "rU").readlines())
                for i, line in enumerate(f.readlines(), 1):
                    line = line.strip("\n").split(",")
                    tlwh = [int(line[2]), int(line[3]), int(line[4]), int(line[5])]
                    self.canvas.update_shape(
                        int(line[1]), int(line[0]), int(line[7]), tlwh, float(line[6]), "L"
                    )
                    if i % 10 == 0:
                        self.sinOut.emit("标注框已加载 {} / {}".format(i, count))
            self.sinOut.emit("标注文件已加载完成")
