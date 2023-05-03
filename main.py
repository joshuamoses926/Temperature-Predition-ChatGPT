import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDateEdit, \
    QVBoxLayout, QWidget, QComboBox
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a widget
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Create a layout
        self.layout = QVBoxLayout(self.main_widget)

        # Create the start and end date widgets
        self.start_date = QDateEdit(self)
        self.end_date = QDateEdit(self)
        self.layout.addWidget(self.start_date)
        self.layout.addWidget(self.end_date)

        # Create a button
        self.button = QPushButton("Show Graph", self)
        self.button.clicked.connect(self.show_graph)
        self.layout.addWidget(self.button)

        # Create a Matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.graph_type = QComboBox(self)
        self.graph_type.addItem("Line Graph")
        self.graph_type.addItem("Bar Graph")
        self.layout.addWidget(self.graph_type)

        # Show the window
        self.show()

    def show_graph(self):
    # Read the CSV data
        df = pd.read_csv("temperatures.csv")

    # Convert the date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

    # Get the start and end dates
        start_date = self.start_date.date().toPyDate()
        end_date = self.end_date.date().toPyDate()

    # Convert the start and end dates to datetime64[ns]
        start_date = np.datetime64(start_date)
        end_date = np.datetime64(end_date)

    # Filter the data based on the selected dates
        filtered_df = df.loc[start_date:end_date]

    # Get the selected graph type
        graph_type = self.graph_type.currentText()

    # Plot the data
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if graph_type == "Line Graph":
            ax.plot(filtered_df.index, filtered_df['Temperature'])
        else:
            ax.bar(filtered_df.index, filtered_df['Temperature'])
        ax.set_xlabel("Date")
        ax.set_ylabel("Temperature (°F)")
        self.canvas.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
