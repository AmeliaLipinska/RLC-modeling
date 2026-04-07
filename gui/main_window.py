import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QLabel, QLineEdit, QFormLayout, QGroupBox, QPushButton)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from signals import signal_sin, signal_square, signal_triangle

from PySide6.QtGui import QDoubleValidator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Symulator RLC")
        self.resize(1200, 600) # a wide window for starters

        #---------------------PICTURE----------------------

       # main widget 
        central_widget = QWidget() #creating an epty widget
        self.setCentralWidget(central_widget) #seting this widget as a main-central widget
        #everything in aplication will be created in central widget
        self.main_layout = QHBoxLayout(central_widget)#lays out widgets in a horizontal row(every vidget created in central will be horisontaly displayed nex to each other)

        #left side of the window
        self.label_picture = QLabel()
        self.label_picture.setAlignment(Qt.AlignCenter) #centered on the left
        
        #loading image into the object

        #building a file path to the image
        pic_path= os.path.join("assets", "RLC.png")
        #loads the pic to an object
        self.original_pixmap = QPixmap(pic_path)#QPixmap is an image container
        
        # adding the pic to the main alignment (stretch) = 3 (makes it 75%)
        self.main_layout.addWidget(self.label_picture, stretch=5)

        #------------------------INPUT-------------------------

        # right side of the window
        # creating vertical setting for the right panel
        self.right_panel = QVBoxLayout()
        
        # Grup Parametry Modelu
        self.group_box = QGroupBox("Parametry Układu") #a box that groups related widgets together
        self.form_layout = QFormLayout()#makes the label on left imput on right

        # imputs parameters to be edited
        self.input_R = QLineEdit()
        self.input_R2 = QLineEdit()
        self.input_L = QLineEdit()
        self.input_C = QLineEdit()

        # adding rows to the menu
        self.form_layout.addRow("Rezystancja R [Ω]:", self.input_R)
        self.form_layout.addRow("Rezystancja R2 [Ω]:", self.input_R2)
        self.form_layout.addRow("Indukcyjność L [H]:", self.input_L)
        self.form_layout.addRow("Pojemność C [F]:", self.input_C)

        self.group_box.setLayout(self.form_layout)#setting  imputs ina  form
        
        # adding the group of right panel
        self.right_panel.addWidget(self.group_box)

        #----------------INPUT SIGANLS BOXES----------------
        self.signal_group = QGroupBox("Typ sygnału")
        self.signal_layout = QVBoxLayout()

        self.button_sin = QPushButton("Sygnał harmoniczny")
        self.button_square = QPushButton("Sygnał prostokątny")
        self.button_triangle = QPushButton("Sygnał trójkątny")

        self.input_A=QLineEdit()
        self.input_F=QLineEdit()

        self.signal_layout.addWidget(self.button_sin)
        self.signal_layout.addWidget(self.button_square)
        self.signal_layout.addWidget(self.button_triangle)

        self.signal_layout.addWidget(QLabel("Amplituda A [V]:"))
        self.signal_layout.addWidget(self.input_A)

        self.signal_layout.addWidget(QLabel("Czestotliwosc [Hz]:"))
        self.signal_layout.addWidget(self.input_F)
        
        self.signal_group.setLayout(self.signal_layout)
        self.right_panel.addWidget(self.signal_group)

        self.button_sin.clicked.connect(signal_sin)
        self.button_square.clicked.connect(signal_square)
        self.button_triangle.clicked.connect(signal_triangle)

        #-----------------VALIDATOR--------------------------

        double_validator = QDoubleValidator()
        double_validator.setBottom(0.0) #>=0

        self.input_R.setValidator(double_validator)
        self.input_R2.setValidator(double_validator)
        self.input_L.setValidator(double_validator)
        self.input_C.setValidator(double_validator)
        
        # so they dont stretch vertically
        self.right_panel.addStretch()

        self.main_layout.addLayout(self.right_panel, stretch=1)

    # funkcja odświeżająca obrazek przy zmianie rozmiaru okna
    def resizeEvent(self, event):
        if not self.original_pixmap.isNull():
            # skalujemy do aktualnego rozmiaru miejsca przeznaczonego na obrazek
            available_size = self.label_picture.size()
            scaled_size = self.original_pixmap.scaled(available_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.label_picture.setPixmap(scaled_size)
        super().resizeEvent(event)