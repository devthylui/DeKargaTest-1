import sys, os

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class loadingFrame(QMainWindow):
    def __init__(self, switch_callback=None):
        super().__init__()

        pix = QPixmap(resource_path("resources/LOGO.png"))

        self.setObjectName("mainFrame")
        self.resize(800, 480)
        self.setWindowOpacity(0.9) 
        
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setStyleSheet("background-color: white;")        
        self.centralwidget.setObjectName("centralwidget")

        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setObjectName("mainLayout")

        self.centerFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.centerFrame.setStyleSheet("QFrame#centerFrame {\n"
            "   background-image: url('./resources/Loading Screen BG.png');\n"
            "   background-position: left;\n"
            "   background-repeat: no-repeat;\n"
            "   background-color: white;\n"
            "   border: 1px solid rgb(156, 163, 175);\n"
            "   border-radius: 5px;\n"
            "   padding: 0px;\n" 
            "}")
        self.centerFrame.setObjectName("centerFrame")
        self.mainLayout.addWidget(self.centerFrame)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centerFrame)
        self.verticalLayout.setObjectName("verticalLayout")

        self.loadingLayout = QtWidgets.QVBoxLayout()

        self.loadingLayout.setSpacing(10) 
        self.loadingLayout.setContentsMargins(0, 0, 0, 0)

        spacerItemTop = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.loadingLayout.addItem(spacerItemTop)
        
        #LOGO
        self.label = QtWidgets.QLabel(parent=self.centerFrame)
        self.label.setStyleSheet("background-color: transparent; margin: 0px; padding: 0px;") 
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum)
        
        target_w, target_h = 550, 300
        self.label.setPixmap(pix.scaled(target_w, target_h, 
                                        QtCore.Qt.AspectRatioMode.KeepAspectRatio, 
                                        QtCore.Qt.TransformationMode.SmoothTransformation))
        self.loadingLayout.addWidget(self.label)

        #DIEGA & TAPPA
        self.logoLabel = QtWidgets.QLabel(parent=self.centerFrame)
        self.logoLabel.setStyleSheet("font: 800 11pt \"Bahnschrift\"; color: rgb(55, 65, 81); background-color: transparent;")
        self.logoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logoLabel.setText("DIEGA & TAPPA")
        self.logoLabel.setFixedHeight(20) 
        self.loadingLayout.addWidget(self.logoLabel)

        #LOADING TEXT
        self.statusLabel = QtWidgets.QLabel(parent=self.centerFrame)
        self.statusLabel.setStyleSheet("font: 500 10pt \"Segoe UI\"; color: rgb(55, 65, 81); background-color: transparent;")
        self.statusLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.statusLabel.setText("Initializing application...")
        self.statusLabel.setFixedHeight(20)
        self.loadingLayout.addWidget(self.statusLabel)

        spacerItemBottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.loadingLayout.addItem(spacerItemBottom)

        self.versionLabel = QtWidgets.QLabel(parent=self.centerFrame)
        self.versionLabel.setStyleSheet("font: 400 8pt \"Segoe UI\"; color: black; background-color: transparent;")
        self.versionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)
        self.versionLabel.setText("Version 1.0.0 | Build B0001") 
        self.loadingLayout.addWidget(self.versionLabel)
        
        self.verticalLayout.addLayout(self.loadingLayout)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi(switch_callback)

    def retranslateUi(self, switch_callback):
        self.setWindowTitle("TruckCane AI")
        self.loadStep = 0
        self.statusMessages = [
            "Initializing Raspberry Pi 5...",
            "Initializing Camera Module...",
            "Initializing Touch Display...",
            "Loading YOLOv11 Model...",
            "Loading GUI..."
        ]
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.fakeLoad(switch_callback))
        self.timer.start(500)

    def fakeLoad(self, switch_callback):
        if self.loadStep < len(self.statusMessages):
            self.statusLabel.setText(self.statusMessages[self.loadStep])
            self.loadStep += 1
        else:
            switch_callback("main")
            self.timer.stop()
