import sys, os
import random

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QComboBox, QStackedWidget, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5 import QtCore  # Import QtCore module
from PyQt5.QtCore import pyqtSignal, QThread

from _src import configus, firework

config_path = 'static/config/config.json'
config_data = configus.load_config(config_path)


def get_select_number_list(menu):
    def powers_of_two(limit):
        power_list = []
        power_of_two = 1
        while power_of_two <= limit:
            power_list.append(power_of_two)
            power_of_two *= 2
        return power_list

    result = powers_of_two(len(menu))
    result_str_covert = list(map(str, result[::-1][:-1]))
    ##print(result_str_covert)
    return result_str_covert


def get_ramdom_menu(menu,number):
    # Select 4 random items from the dictionary
    selected_items = random.sample(list(menu.items()), number)

    ##print(dict(selected_items))
    return dict(selected_items)

class ImagePushButton(QPushButton):
    clicked_with_label = pyqtSignal(str)  # Define a signal that emits a string when clicked

    def __init__(self, pixmap_path, label_name):
        super().__init__()
        self.label_name = label_name
        pixmap = QPixmap(pixmap_path)
        icon = QIcon(pixmap)
        self.setIcon(icon)
        self.setIconSize(pixmap.size())
        self.setFixedSize(400, 500)  # Set size to 400x500 pixels
        self.setStyleSheet("border: none;")  # Remove border
        self.clicked.connect(self.emit_label_name)
    
    def emit_label_name(self):
        self.clicked_with_label.emit(self.label_name)  # Emit the label name when clicked

class choice_menu(QWidget):
    def __init__(self, two_menu):
        super().__init__()
        self.two_menu = two_menu

        page2_layout = QHBoxLayout()  
        self.setLayout(page2_layout)

        self.image_button1_layout = QVBoxLayout()
        self.image_button1 = ImagePushButton(os.path.join('static', 'img', config_data['menu'][two_menu[0]]), two_menu[0])
        self.image_button1_layout.addWidget(self.image_button1)
        label1 = QLabel(two_menu[0])  # Add label for button 1
        label1.setAlignment(QtCore.Qt.AlignCenter)  # Align label centrally
        label1.setFont(QFont("Lucida Console", 15))  # Set font for label 1
        self.image_button1_layout.addWidget(label1)
        page2_layout.addLayout(self.image_button1_layout)

        self.image_button2_layout = QVBoxLayout()
        self.image_button2 = ImagePushButton(os.path.join('static', 'img', config_data['menu'][two_menu[1]]), two_menu[1])
        self.image_button2_layout.addWidget(self.image_button2)
        label2 = QLabel(two_menu[1])  # Add label for button 2
        label2.setAlignment(QtCore.Qt.AlignCenter)  # Align label centrally
        label2.setFont(QFont("Lucida Console", 15))  # Set font for label 2
        self.image_button2_layout.addWidget(label2)
        page2_layout.addLayout(self.image_button2_layout)


class FireworksThread(QThread):
    finished_signal = pyqtSignal()

    def run(self):
        firework.show_fireworks_on_screen(1)
        self.finished_signal.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.menu = {}
        self.sorted_menu = []
        self.choiced_menu = []
        self.cnt_currunt_menu = 0
        
        self.selected_number = 0
        self.setWindowTitle("Idea World Cup v0.2")
        self.resize(800, 600)  # Set the size of the main window

        # Set window title font using style sheet
        self.setStyleSheet("font-family: 'Lucida Console', monospace;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create the main layout
        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        # Create a stacked widget to switch between pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Page 1: Idea Submission
        self.main_widget = QWidget()
        page1_layout = QVBoxLayout()
        self.main_widget.setLayout(page1_layout)

        image_label = QLabel()
        pixmap = QPixmap(os.path.join('static','img',config_data['main']))  # Replace "path/to/your/image.jpg" with the actual path to your image
        image_label.setPixmap(pixmap)
        image_label.setAlignment(QtCore.Qt.AlignCenter)   # Set alignment to center
        page1_layout.addWidget(image_label)

        label = QLabel("How many items do you want?")
        page1_layout.addWidget(label)

        self.combo_box = QComboBox()
        self.combo_box.addItems(get_select_number_list(config_data['menu']))
        page1_layout.addWidget(self.combo_box)

        submit_button = QPushButton("Start")
        submit_button.clicked.connect(self.define_menu)
        page1_layout.addWidget(submit_button)
        self.stacked_widget.addWidget(self.main_widget)

    def define_menu(self):
        self.selected_number = self.combo_box.currentText()
        self.menu = get_ramdom_menu(config_data['menu'],int(self.selected_number))
        #print(self.selected_number)
        #print(self.menu)
        self.sorted_menu = list(self.menu.keys())
        self.goto_choice_menu(self.sorted_menu)
    
    def goto_choice_menu(self, list_menu):
        self.choice_menu(list_menu[:2])

    def choice_menu(self, two_menu):
        # Page 2: Selectable Images
        self.choice_menu_widget = choice_menu(two_menu)
        self.stacked_widget.addWidget(self.choice_menu_widget)
        self.stacked_widget.setCurrentWidget(self.choice_menu_widget)

        # Connect the signals from ImagePushButton to slots in MainWindow
        self.choice_menu_widget.image_button1.clicked_with_label.connect(self.handle_button_click)
        self.choice_menu_widget.image_button2.clicked_with_label.connect(self.handle_button_click)
    
    def show_winner_message(self, label_name):
        winner_msg_box = QMessageBox()
        winner_msg_box.setWindowTitle("Winner!!!!")
        
        label_img = QLabel()
        pixmap = QPixmap(os.path.join('static', 'img', config_data['menu'][label_name]))
        label_img.setPixmap(pixmap)
        winner_msg_box.layout().addWidget(label_img)

        winner_label = QLabel(config_data['menu_kor'][label_name])
        winner_label.setFont(QFont("Lucida Console", 15))
        winner_msg_box.layout().addWidget(winner_label)
        
        # Connect finished signal to quit application
        winner_msg_box.finished.connect(self.quit_application)
        winner_msg_box.exec_()


    def quit_application(self):
        QApplication.quit()

    def handle_button_click(self, label_name):
        #print(f'handle_button_click / self.sorted_menu - {self.sorted_menu}')
        # Handle the button click event
        self.choiced_menu.append(label_name)
        self.sorted_menu = self.sorted_menu[2:]
        if len(self.sorted_menu) != 0:
            self.choice_menu(self.sorted_menu)
        if len(self.sorted_menu) == 0:
            if len(self.choiced_menu) != 1:
                msg_box = QMessageBox()
                msg_box.setWindowTitle(f"Round{self.selected_number} done!")
                msg_box.setText(f"<div align='center'>Round {self.selected_number} is Done</div>")
                msg_box.setFont(QFont("Lucida Console", 15))
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                self.sorted_menu = self.choiced_menu
                self.choiced_menu = []
                self.selected_number = str(int(int(self.selected_number)/2))
                #print(self.sorted_menu)
                self.goto_choice_menu(self.sorted_menu)
            else:
                self.show_winner_message(self.choiced_menu[0])
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
