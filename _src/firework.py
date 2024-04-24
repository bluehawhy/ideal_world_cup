import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer, QPoint
import random
import math

class FireworksWidget(QWidget):
    def __init__(self, screen_geometry):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle('Fireworks')
        self.fireworks = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.createFirework)
        self.timer.start(1000)  # Adjust the interval as needed
        # Create a timer to quit after 10 seconds
        self.quit_timer = QTimer(self)
        self.quit_timer.timeout.connect(QApplication.instance().quit)
        self.quit_timer.start(15000)  # 15s seconds

        self.setGeometry(screen_geometry)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for firework in self.fireworks:
            firework.draw(painter)

    def createFirework(self):
        x = random.randint(0, self.width())
        y = random.randint(0, self.height())
        self.fireworks.append(Firework(x, y, self))

class Firework:
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent
        self.timer = QTimer(self.parent)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # Adjust the interval as needed
        self.radius = 0
        self.color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self):
        self.radius += 2
        if self.radius > 100:  # Maximum radius for the firework
            self.parent.fireworks.remove(self)

        self.parent.update()

    def draw(self, painter):
        pen = QPen(self.color)
        pen.setWidth(3)
        painter.setPen(pen)
        # Draw petals
        for angle in range(0, 360, 30):
            x1 = int(self.x + self.radius * math.cos(math.radians(angle)))
            y1 = int(self.y + self.radius * math.sin(math.radians(angle)))
            x2 = int(self.x + (self.radius * 0.6) * math.cos(math.radians(angle + 15)))
            y2 = int(self.y + (self.radius * 0.6) * math.sin(math.radians(angle + 15)))
            painter.drawLine(QPoint(x1, y1), QPoint(x2, y2))
        # Draw center
        painter.drawEllipse(QPoint(int(self.x), int(self.y)), int(self.radius / 10), int(self.radius / 10))

def show_fireworks_on_screen(screen_index):
    app = QApplication(sys.argv)

    # Get the desktop widget
    desktop = app.desktop()
    # Get the number of screens
    num_screens = desktop.screenCount()

    # Check if the requested screen index is valid
    if screen_index >= num_screens:
        print("Invalid screen index!")
        sys.exit(1)

    # Get the geometry of the specified screen
    screen_geometry = desktop.screenGeometry(screen_index)

    fireworks_widget = FireworksWidget(screen_geometry)
    fireworks_widget.showFullScreen()

    sys.exit(app.exec_())

if __name__ == '__main__':
    # Example: Display fireworks on the second screen (index 1)
    show_fireworks_on_screen(1)
