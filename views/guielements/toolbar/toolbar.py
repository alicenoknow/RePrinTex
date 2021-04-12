from PyQt5.QtWidgets import QAction, QToolBar

from controllers.guielements.toolbar_controller import ToolBarController


# TODO zoom nie działa xD


class ToolBar:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ToolBarController(parent)
        self.toolbar = QToolBar("Tools", self.parent)
        self.toolbar.addActions(self.get_actions())

    def get_actions(self):
        actions = [self.undo(), self.zoom_in(), self.zoom_out(),self.analyze_image(),self.recognize_letters(), self.clean(), self.contrast()]
        return actions

    def analyze_image(self):
        analyze_image = QAction("&Analyze image",self.parent)

        analyze_image.setShortcut('Ctrl+a')
        analyze_image.setStatusTip("Analyze image: find text block, words and characters, determine upper and lower bounds of text lines.")
        analyze_image.triggered.connect(lambda: self.controller.analyze_text())
        return analyze_image

    def recognize_letters(self):
        recognize_letters = QAction("&Recognize letters",self.parent)

        recognize_letters.setShortcut('Ctrl+Shift+a')
        recognize_letters.setStatusTip("Recognize letters: Perform image image analyze, fill letters set and recognize letters on the image.")
        recognize_letters.triggered.connect(lambda: self.controller.recognize_letters())
        return recognize_letters

    def zoom_in(self):
        zoom_in = QAction("&Zoom in", self.parent)
        # zoomIn = QAction(QIcon("zoomIn.bmp"),"Zoom in",self) <- too jak zrobimy ikonki kiedyś

        zoom_in.setShortcut('Ctrl+u')
        zoom_in.setStatusTip("Zoom in")
        zoom_in.triggered.connect(lambda: self.controller.zoom_in())  # jak sie da to od razu self.controller.zoom(1.1)
        return zoom_in

    def zoom_out(self):
        zoom_out = QAction("&Zoom out", self.parent)
        # zoomOut = QAction(QIcon("zoomOut.bmp"),"Zoom out",self) <- too jak zrobimy ikonki kiedyś

        zoom_out.setShortcut('Ctrl+i')
        zoom_out.setStatusTip("Zoom out")
        zoom_out.triggered.connect(lambda: self.controller.zoom_out())
        return zoom_out

    def clean(self):
        clean = QAction("&Clean", self.parent)
        clean.triggered.connect(lambda: self.controller.clean())
        return clean

    def contrast(self):
        contrast = QAction("&Contrast", self.parent)
        contrast.triggered.connect(lambda: self.controller.contrast())
        return contrast

    def rotate(self):
        pass

    def undo(self):
        undo = QAction("&Undo", self.parent)
        undo.triggered.connect(lambda: self.controller.undo())
        return undo

    def get_toolbar(self):
        return self.toolbar
