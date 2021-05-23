from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QCursor

import cv2
import os

from controllers.controller import Controller
from imgmaneng.img_cleaner import clean_page, increase_contrast
from imgmaneng.lines_streightening import lines_streigtening
from models.effects import EffectType
from services.images_provider import ImagesProvider
from threads.worker_decorator import multi_thread_runner


class EffectsController:
    """
    A class for handling effects on images
    Attributes
        parent: QMainWindow
        view: EffectsView
    """

    def __init__(self, parent, view) -> None:
        self.parent = parent
        self.view = view
        # img = parent.image_preview_view.controller.current_image
        self.image_provider = ImagesProvider()
        Controller().set_effects_controller(self)

    def clean(self, img):
        clean = clean_page(img, self.modified_effects.upper_shift, self.modified_effects.lower_shift)
        return clean

    def contrast(self, img):
        clean = increase_contrast(img, self.modified_effects.contrast_intensity)
        return clean

    def straighten_lines(self, img):
        straight = lines_streigtening(img)
        return straight

    @multi_thread_runner
    def apply(self, image=None, path=None):
        if image is None:
            image = ImagesProvider().create_new_reworked_image()
        if path is None:
            name = ImagesProvider().get_current_image_name()
            directory = str(QtWidgets.QFileDialog.getExistingDirectory())
            path = directory + "/" + name + "_converted.png"
        cv2.imwrite(path, image)

    @multi_thread_runner
    def apply_all(self):
        C = ImagesProvider().get_current_collection()
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        new_dir = directory + "/" + C.name

        try:
            os.mkdir(new_dir)
        except OSError:
            Controller().communicator.error.emit("Cannot create a directory!")
            return

        for image in C.collection:
            new_image = ImagesProvider().create_new_reworked_image(image)
            path = new_dir + "/" + image.name + "_converted.png"
            self.apply(new_image, path)

    def is_brush_active(self):
        return self.view.stains_button.isChecked()

    def get_brush_radius(self):
        return self.view.stains_slider.value()

    @multi_thread_runner
    def change_effects(self, effects_to_change):  # {effect_type:EffectType,type:Line,org:bool, value:bool}
        effects = ImagesProvider().get_current_collection_effects()
        if effects_to_change['org']:
            if effects_to_change['type'] not in ImagesProvider().get_current_collection_org_lines():
                ImagesProvider().get_current_collection_org_lines().add(effects_to_change['type'])
            else:
                ImagesProvider().get_current_collection_org_lines().remove(effects_to_change['type'])
        elif effects_to_change['effect_type'] == EffectType.LINES:
            if effects_to_change['type'] not in effects.values[EffectType.LINES.value]:
                effects.values[EffectType.LINES.value][effects_to_change['type']] = True
            else:
                effects.values[EffectType.LINES.value].pop(effects_to_change['type'])
            print(effects.values[EffectType.LINES.value])
        else:
            for eff in effects_to_change['values']:
                if eff['type'] == EffectType.CORRECTIONS:
                    effects.values[eff['type'].value].append(eff['value'])
                else:
                    effects.values[eff['type'].value] = eff['value']
        ImagesProvider().update_displayed_images(effects_to_change['org'])

    def change_cursor(self):
        if self.is_brush_active():
            pixmap = QPixmap("data/cursors/circle_cursor.png")
            size = 3 * self.get_brush_radius() * Controller().get_modified_zoom()
            pixmap = pixmap.scaled(size, size)
            cursor = QCursor(pixmap, -1, -1)
            self.parent.setCursor(cursor)
        else:
            self.parent.setCursor(QtCore.Qt.ArrowCursor)
