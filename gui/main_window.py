import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QGridLayout, QVBoxLayout, 
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
        self.resize(1700, 900)

       #---------------------WINDOW-----------------

       # main widget 
        central_widget = QWidget() #creating an epty widget
        self.setCentralWidget(central_widget) #seting this widget as a main-central widget
        #everything in aplication will be created in central widget
        self.main_layout = QVBoxLayout(central_widget)#lays out widgets in a horizontal row(every vidget created in central will be horisontaly displayed nex to each other)
        
        self.top_layout = QHBoxLayout()
        self.plot_grid = QGridLayout()
        
        self.main_layout.addLayout(self.top_layout, stretch=3)
        self.main_layout.addLayout(self.plot_grid)

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
        self.input_L.setText("0,33")
        self.input_C = QLineEdit()
        self.input_C.setText("0,0000001")

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
        self.input_F.setText("500")
        self.input_D=QLineEdit()
        self.input_D.setText("0,5")

        self.signal_layout.addWidget(self.button_sin)
        self.signal_layout.addWidget(self.button_square)
        self.signal_layout.addWidget(self.button_triangle)

        self.signal_layout.addWidget(QLabel("Amplituda A [V]:"))
        self.signal_layout.addWidget(self.input_A)

        self.signal_layout.addWidget(QLabel("Czestotliwosc [Hz]:"))
        self.signal_layout.addWidget(self.input_F)

        self.signal_layout.addWidget(QLabel("Wypełnienie (0-1):"))
        self.signal_layout.addWidget(self.input_D)

        self.input_T = QLineEdit()
        self.input_T.setText("0,01")
        self.signal_layout.addWidget(QLabel("Czas symulacji [s]:"))
        self.signal_layout.addWidget(self.input_T)
        
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

        # -------------------BODE PLOT CANVAS-----------------------
        self.fig_mag = Figure()
        self.canvas_mag = FigureCanvas(self.fig_mag)
        self.ax_mag = self.fig_mag.add_subplot(111)

        self.fig_phase = Figure()
        self.canvas_phase = FigureCanvas(self.fig_phase)
        self.ax_phase = self.fig_phase.add_subplot(111)

        # adding to the grid
        self.plot_grid.addWidget(self.canvas_input, 0, 0)   # Top-Left
        self.plot_grid.addWidget(self.canvas_output, 0, 1)  # Top-Right
        self.plot_grid.addWidget(self.canvas_mag, 1, 0)     # Bottom-Left (Under Input)
        self.plot_grid.addWidget(self.canvas_phase, 1, 1)   # Bottom-Right (Under Output)
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
        self.input_T.setValidator(double_validator)
        
        # so they dont stretch vertically
        self.right_panel.addStretch()

        self.top_layout.addLayout(self.right_panel, stretch=1)



    #plotting
    def input_plot(self, signal_function, t_end, start_time=0):
        t=np.linspace(0,t_end,1000)
        y=signal_function(t)
             
        #drawing the signal
        self.ax_input.clear()
        self.ax_input.plot(t, y)
        self.ax_input.grid(True)
        self.ax_input.set_title("INPUT SIGNAL")
        self.canvas_input.draw()

    def output_plot(self, t_param, y_param):
        self.ax_output.clear()
        self.ax_output.plot(t_param, y_param)
        self.ax_output.grid(True)
        self.ax_output.set_title("OUTPUT SIGNAL")
        self.canvas_output.draw()

    def plot_bode(self):
        from scipy import signal
        import numpy as np

        R = float(self.input_R.text().replace(",", "."))
        R2 = float(self.input_R2.text().replace(",", "."))
        C = float(self.input_C.text().replace(",", "."))
        
        # Transfer Function coefficients: G(s) = num / den
        # G(s) = (R / (R + R2)) / ( (R*R2*C)/(R+R2) * s + 1 )
        num_coeff = R / (R + R2)
        den_coeff = (R * R2 * C) / (R + R2)
        
        num = [num_coeff]
        den = [den_coeff, 1]

        sys = signal.lti(num, den)
        w = np.logspace(1, 6, 500) 
        w, mag, phase = signal.bode(sys, w=w)
        freq_hz = w / (2 * np.pi)

        # Magnitude Plot
        self.ax_mag.clear()
        self.ax_mag.semilogx(freq_hz, mag, color='crimson')
        self.ax_mag.grid(True, which="both", ls="--")
        self.ax_mag.set_ylabel("Mag [dB]")
        self.fig_mag.tight_layout()
        self.canvas_mag.draw()

        # Phase Plot
        self.ax_phase.clear()
        self.ax_phase.semilogx(freq_hz, phase, color='royalblue')
        self.ax_phase.grid(True, which="both", ls="--")
        self.ax_phase.set_ylabel("Phase [deg]")
        self.ax_phase.set_xlabel("Frequency [Hz]")
        self.fig_phase.tight_layout()
        self.canvas_phase.draw()

    #connecting the button
    def clicked_on_sin(self):
        amp=float(self.input_A.text().replace(",", ".")) #input_A->text->float
        freq=float(self.input_F.text().replace(",", "."))

        f=signal_sin(amp, freq)

        #output/input
        t, y = self.simulation(f)
        self.input_plot(f, t[-1])
        self.output_plot(t, y)
        self.plot_bode()
    
    def clicked_on_square(self):
        amp=float(self.input_A.text().replace(",", "."))
        freq=float(self.input_F.text().replace(",", "."))
        duty=float(self.input_D.text().replace(",", "."))

        delay = 0.0001

        f=signal_square(amp, freq, duty, start_time=delay)

        #output/input
        t, y=self.simulation(f)
        self.input_plot(f, t[-1], start_time = delay)
        self.output_plot(t, y)
        self.plot_bode()
    
    def clicked_on_triangle(self):
        amp=float(self.input_A.text().replace(",", "."))
        freq=float(self.input_F.text().replace(",", "."))

        f=signal_triangle(amp, freq)

        #output/input
        t, y=self.simulation(f)
        self.input_plot(f, t[-1])
        self.output_plot(t, y)
        self.plot_bode()

    def simulation(self, signal_function):
        import numpy as np
        from rk45 import rk4_step
        from model import circuit_model

        freq=float(self.input_F.text().replace(",", "."))

        t_end = float(self.input_T.text().replace(",", "."))

        #simulation time
        t=0.0
        
        total_steps = 5000
        h= t_end/total_steps
        
        # starting state
        x=np.array([0.0, 0.0])

        #parameters
        R=float(self.input_R.text().replace(",", "."))
        R2=float(self.input_R2.text().replace(",", "."))
        L=float(self.input_L.text().replace(",", "."))
        C=float(self.input_C.text().replace(",", "."))

        parameters = [L, R2, C, R]

        #saving place for the graph

        t_values = np.zeros(total_steps)
        y_values= np.zeros(total_steps)

        #simulation rk4
        for i in range(total_steps):
            x = rk4_step(t, x, h, signal_function, parameters)
            _, y, _ = circuit_model(t, x, signal_function(t), parameters)
            t_values[i] = t
            y_values[i]=(float(y.flatten()[0]))
            t += h

        if total_steps > 2000:
            downsample_factor = total_steps // 2000
            t_values = t_values[::downsample_factor].tolist()
            y_values = y_values[::downsample_factor].tolist()
        else:
            t_values = t_values.tolist()
            y_values = y_values.tolist()

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