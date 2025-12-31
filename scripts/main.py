from mainFrame import mainFrame
from cameraFrame import cameraFrame
from analysisFrame import analysisFrame
from filesFrame import filesFrame
from loadingFrame import loadingFrame
from viewFrame import viewFrame

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

#SS
from PyQt6.QtGui import QShortcut, QKeySequence 
import datetime
import os

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TruckCane AI")
        self.setFixedSize(800, 416)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.mainFrame = mainFrame(self.switch_screen)
        self.cameraFrame = cameraFrame(self.switch_screen)
        self.analysisFrame = analysisFrame(self.switch_screen)
        self.filesFrame = filesFrame(self.switch_screen)
        self.viewFrame = viewFrame(self.switch_screen)

        self.lastWidget = None
        self.loadingFrame = loadingFrame(self.switch_screen)
        self.stack.addWidget(self.loadingFrame)
        self.stack.setCurrentWidget(self.loadingFrame)
        self.lastWidget = self.loadingFrame

    #SS
        self.screenshot_shortcut = QShortcut(QKeySequence("F12"), self)
        self.screenshot_shortcut.activated.connect(self.take_screenshot)  

    def take_screenshot(self):
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/TruckCane_{timestamp}.png"

        self.grab().save(filename)
        print(f"Captured: {filename}")      

    def switch_screen(self, name, qt_img=None, timestamp=None, results=None, sauce=None):
        if self.lastWidget != None:
            self.stack.removeWidget(self.lastWidget)
        match name:
            case "main":
                self.stack.addWidget(self.mainFrame)
                self.stack.setCurrentWidget(self.mainFrame)
                self.lastWidget = self.mainFrame
            case "camera":
                self.stack.addWidget(self.cameraFrame)
                self.stack.setCurrentWidget(self.cameraFrame)
                self.cameraFrame.resumeCam()
                self.lastWidget = self.cameraFrame
            case "analysis":
                self.stack.addWidget(self.analysisFrame)
                self.stack.setCurrentWidget(self.analysisFrame)
                self.analysisFrame.loadImage(qt_img, timestamp, sauce)
                self.lastWidget = self.analysisFrame
            case "view":
                self.stack.addWidget(self.viewFrame)
                self.stack.setCurrentWidget(self.viewFrame)
                self.viewFrame.loadImage(qt_img, timestamp, results, sauce)
                self.lastWidget = self.viewFrame
            case "settings":
                self.stack.addWidget(self.settingsFrame)
                self.stack.setCurrentWidget(self.settingsFrame)
                self.lastWidget = self.settingsFrame
            case "files":
                self.stack.addWidget(self.filesFrame)
                self.stack.setCurrentWidget(self.filesFrame)
                self.filesFrame.refreshList(self.switch_screen)
                self.lastWidget = self.filesFrame

if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec()
