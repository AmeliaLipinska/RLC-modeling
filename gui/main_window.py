import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QLabel, QLineEdit, QFormLayout, QGroupBox, QPushButton)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from signals import signal_sin, signal_square, signal_triangle

from PySide6.QtGui import QDoubleValidator

import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Symulator RLC")
        self.resize(1200, 600) # a wide window for starters

       #---------------------WINDOW-----------------

       # main widget 
        central_widget = QWidget() #creating an epty widget
        self.setCentralWidget(central_widget) #seting this widget as a main-central widget
        #everything in aplication will be created in central widget
        self.main_layout = QVBoxLayout(central_widget)#lays out widgets in a horizontal row(every vidget created in central will be horisontaly displayed nex to each other)

        #making an upper and lower layout
        self.top_layout = QHBoxLayout()
        self.main_layout.addLayout(self.top_layout, stretch=2)

        self.bottom_layout =QHBoxLayout()
        self.main_layout.addLayout(self.bottom_layout, stretch=1)

        #---------------------PICTURE----------------------
        #left side of the window
        self.label_picture = QLabel()
        self.label_picture.setAlignment(Qt.AlignCenter) #centered on the left
        
        #loading image into the object

        #building a file path to the image
        pic_path= os.path.join("assets", "RLC.png")
        #loads the pic to an object
        self.original_pixmap = QPixmap(pic_path)#QPixmap is an image container
        
        # adding the pic to the top alignment (stretch) = 3 (makes it 75%)
        self.top_layout.addWidget(self.label_picture, stretch=5)

        #------------------------INPUT-------------------------

        # right side of the window
        # creating vertical setting for the right panel
        self.right_panel = QVBoxLayout()
        
        # Grup Parametry Modelu
        self.group_box = QGroupBox("Parametry Układu") #a box that groups related widgets together
        self.form_layout = QFormLayout()#makes the label on left imput on right

        # imputs parameters to be edited
        self.input_R = QLineEdit()
        self.input_R.setText("1000")
        self.input_R2 = QLineEdit()
        self.input_R2.setText("1000")
        self.input_L = QLineEdit()
        self.input_L.setText("0,0000001")
        self.input_C = QLineEdit()
        self.input_C.setText("0,01")

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
        self.input_A.setText("5")
        self.input_F=QLineEdit()
        self.input_F.setText("5000")
        self.input_D=QLineEdit()
        self.input_D.setText("100")

        self.signal_layout.addWidget(self.button_sin)
        self.signal_layout.addWidget(self.button_square)
        self.signal_layout.addWidget(self.button_triangle)

        self.signal_layout.addWidget(QLabel("Amplituda A [V]:"))
        self.signal_layout.addWidget(self.input_A)

        self.signal_layout.addWidget(QLabel("Czestotliwosc [Hz]:"))
        self.signal_layout.addWidget(self.input_F)

        self.signal_layout.addWidget(QLabel("Czas trwania protokątnego [s]:"))
        self.signal_layout.addWidget(self.input_D)
        
        self.signal_group.setLayout(self.signal_layout)
        self.right_panel.addWidget(self.signal_group)

        self.button_sin.clicked.connect(self.clicked_on_sin)
        self.button_square.clicked.connect(self.clicked_on_square)
        self.button_triangle.clicked.connect(self.clicked_on_triangle)

        #-----------------SIMULATION OF INPUT SIGNAL-------------
        import time
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.figure import Figure

        #setting the back
        self.input_figure = Figure() #creating a clear paper
        self.canvas_input = FigureCanvas(self.input_figure)#allows to use figure in gui
        self.ax_input = self.input_figure.add_subplot(111) #creating axes (111)-rzad, kolumna, wykres - jeden wykres na całej figurze

        #-------------------SIMULATION OF OUTPUT SIGNAL------------
        self.output_figure = Figure()
        self.canvas_output = FigureCanvas(self.output_figure)
        self.ax_output = self.output_figure.add_subplot(111)

        #adding to gui
        self.bottom_layout.addWidget(self.canvas_input)
        self.bottom_layout.addWidget(self.canvas_output)
        #-----------------VALIDATOR--------------------------

        double_validator = QDoubleValidator()
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        double_validator.setBottom(0.0) #>=0

        self.input_R.setValidator(double_validator)
        self.input_R2.setValidator(double_validator)
        self.input_L.setValidator(double_validator)
        self.input_C.setValidator(double_validator)
        self.input_A.setValidator(double_validator)
        self.input_F.setValidator(double_validator)
        self.input_D.setValidator(double_validator)
        
        # so they dont stretch vertically
        self.right_panel.addStretch()

        self.top_layout.addLayout(self.right_panel, stretch=1)

    #plotting
    def input_plot(self, signal_function):
        t=np.linspace(0,1,1000)
        y=signal_function(t)
             
        #drawing the signal
        self.ax_input.clear()
        self.ax_input.plot(t, y)
        self.ax_input.set_title("INPUT SIGNAL")
        self.canvas_input.draw()

    def output_plot(self, t_param, y_param):
        self.ax_output.clear()
        self.ax_output.plot(t_param, y_param)
        self.ax_output.set_title("OUTPUT SIGNAL")
        self.canvas_output.draw()

    #connecting the button
    def clicked_on_sin(self):
        amp=float(self.input_A.text().replace(",", ".")) #input_A->text->float
        freq=float(self.input_F.text().replace(",", "."))

        f=signal_sin(amp, freq)
        
        #input
        self.input_plot(f)

        #output
        t, y = self.simulation(f)

        self.output_plot(t, y)
    
    def clicked_on_square(self):
        amp=float(self.input_A.text().replace(",", "."))
        freq=float(self.input_F.text().replace(",", "."))
        dura=float(self.input_D.text().replace(",", "."))

        f=signal_square(amp, freq, dura)

        #input
        self.input_plot(f)

        #output
        t, y=self.simulation(f)

        self.output_plot(t, y)
    
    def clicked_on_triangle(self):
        amp=float(self.input_A.text().replace(",", "."))
        freq=float(self.input_F.text().replace(",", "."))

        f=signal_triangle(amp, freq)

        #input
        self.input_plot(f)

        #output
        t, y=self.simulation(f)

        self.output_plot(t, y)

    def simulation(self, signal_function):
        import numpy as np
        from rk45 import rk45_step
        from model import circuit_model

        freq=float(self.input_F.text().replace(",", "."))

        if freq > 0:
            t_end = 5 / freq 
        else:
            t_end = 0.1

        #simulation time
        t=0
        h=t_end/1000

        # starting state
        x=np.array([0.0, 0.0])

        #parameters
        R=float(self.input_R.text().replace(",", "."))
        R2=float(self.input_R2.text().replace(",", "."))
        L=float(self.input_L.text().replace(",", "."))
        C=float(self.input_C.text().replace(",", "."))

        parameters = [L, R2, C, R]

        #saving place for the graph

        t_values=[]
        y_values=[]

        #simulation
        while t<t_end:
            x, error = rk45_step(t, x, h, signal_function, parameters)

            x=np.array(x).flatten()

            from model import circuit_model

            _,y,_=circuit_model(t,x, signal_function(t),parameters)

            t_values.append(t) #adds element to the end of the list
            y_values.append(np.array(y).flatten()[0])

            t+=h
        return t_values, y_values
        
    # funkcja odświeżająca obrazek przy zmianie rozmiaru okna
    def resizeEvent(self, event):
        if not self.original_pixmap.isNull():
            # skalujemy do aktualnego rozmiaru miejsca przeznaczonego na obrazek
            available_size = self.label_picture.size()
            scaled_size = self.original_pixmap.scaled(available_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.label_picture.setPixmap(scaled_size)
        super().resizeEvent(event)