import os
import random
import re
import string
from typing import List

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox, QListWidget, QListWidgetItem, QDialog

from models.effects import Effects
from models.image import Image


class ImageCollection:
    def __init__(self, name=None, parent=None, path=None):
        self.parent = parent
        self.name = name

        self.detail_file_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(20))
        self.collection: List[Image] = []
        self.effects: Effects = Effects()
        self.lines_on_org = set()
        self.current_image_id = None
        if path:
            self.path = path
            self.detect_images()

    def detect_images(self):
        filenames = os.listdir(self.path)
        img_files = [file for file in filenames if self.check_img_ext(file)]
        for img in img_files:
            print(self.path + '/' + img)
            self.add_image(Image(len(self.collection), self.path + '/' + img, img.split('.')[0],
                                 QPixmap(QImage(self.path + '/' + img))))

    def check_img_ext(self, file):
        for regex in Image.img_ext:
            x = re.search(regex, file)
            if x:
                return True
        return False

    def add_image(self, image):
        self.collection.append(image)

    def clear(self):
        self.current_image_id = None
        self.collection = []

    def get_image_elements(self, idx):
        return self.collection[idx].pixmap, self.collection[idx].name

    def change_current_image(self, idx) -> Image:
        self.current_image_id = idx
        return self.collection[idx]

    def get_current_pixmap(self) -> QPixmap:
        return self.collection[self.current_image_id].pixmap

    def get_current_image(self) -> Image:
        return self.collection[self.current_image_id]
