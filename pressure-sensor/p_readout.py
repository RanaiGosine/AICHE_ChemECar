#AUTHOR: Matthew Ocando

import tkinter as tk
from tkinter import ttk,messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

import serial
import os
import sys


class TtestFrame(ttk.Frame):
    """Tkinter Frame containing relevant widgets"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid(row=0, column=0)
        
        #tk variables
        #self.this_is_a_string = tk.StringVar()

        #Ardiuino variables
        self.arduino_port = "COM5"
        self.baud = 115200
        self.ser = serial.Serial(self.arduino_port, self.baud)
        self.fileName = "pressure-data.csv"

        #temporary variables for plotting test Graph
        self.counter = 0
        self.x=[]
        self.y=[]

        #marker variables
        self.begin = False
        self.end = False

        #seaborn realted variables
        sns.set_style('whitegrid')
        sns.set_palette('deep')
        self.red = sns.xkcd_rgb['vermillion']
        self.blue = sns.xkcd_rgb['dark sky blue']
        self.green = sns.xkcd_rgb['leaf green']

        #matplotlib related variables
        self.fig, self.ax = plt.subplots()

        self.makewidgets()
    
    def makewidgets(self):
        """Creates widgets in TtestFrame

        returns: Nothing."""

        ttk.Label(self, text='Pressure Readout Graph',font=16).grid(row=0,column=0,sticky=tk.W)
        ttk.Button(self, text='START READOUT',command=self.start_readout).grid(row=2, column=0, sticky=tk.W)
        ttk.Button(self, text='STOP READOUT',command=self.stop_readout).grid(row=2, column=1, sticky=tk.W)
        ttk.Button(self, text='Predict',command=self.ml).grid(row=2,column=2,sticky=tk.W)
        ttk.Button(self, text = 'RESTART', command = self.restart).grid(row=3, column =0, sticky = tk.W)
        #ttk.Label(self, text='Group B').grid(row=0,column=1)
        #ttk.Label(self, text='p value = ').grid(row=1,column=1, sticky=tk.S+tk.W)
        #ttk.Entry(self, textvariable=self.this_is_a_string).grid(row=1,column=1,sticky=tk.S)
        #self.group_a = tk.Text(self, width=40, height=10)
        #self.group_b = tk.Text(self, width=40, height=10)
        #self.group_a.grid(row=1, column=0, padx=3, pady=10, sticky=tk.N)
        #self.group_b.grid(row=1, column=1, padx=3, pady=10, sticky=tk.N)

        self.canvas = FigureCanvasTkAgg(self.fig, self)  
        self.canvas.get_tk_widget().grid(column=0, row=1, columnspan=5, sticky=tk.N+tk.S+tk.W+tk.E)
        self.canvas.draw()
        self.ax.set(xlabel='Time (ms)', ylabel='Pressure (Pa)')
        self.ax.grid(b=True)

        #Adding a nav bar
        toolbar_frame = ttk.Frame(self)
        toolbar_frame.grid(column=2, row=3, columnspan=5, sticky=tk.W)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()

    # def perform_test(self):
    #     """Performs t-test and calculates p value

    #     returns: Nothing."""

    #     try:
    #         a_list = self.group_a.get('1.0','end').strip().split()
    #         b_list = self.group_b.get('1.0','end').strip().split()
    #         a_list = [float(i) for i in a_list]
    #         b_list = [float(i) for i in b_list]
    #         combined_list = a_list + b_list
    #         self.diff_measured = np.mean(a_list) - np.mean(b_list) 

    #         self.differences = []
    #         num_simulations = 10000
    #         for i in range(num_simulations):
    #             np.random.shuffle(combined_list)
    #             a_list = combined_list[:len(a_list)]
    #             b_list = combined_list[len(a_list):]
    #             group_a_mean = np.mean(a_list)
    #             group_b_mean = np.mean(b_list)
    #             self.differences.append(group_a_mean - group_b_mean)

    #         self.p_value = sum(diff >= self.diff_measured for diff in self.differences) / num_simulations
    #         self.plot_results()
    #     except:
    #         messagebox.showerror(message='Data must be space-separated, positive numbers!')

    def restart(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def start_readout(self):
        """collects pressure data and plots

        returns: Nothing."""
        
        #Arduino code
        self.getData = str(self.ser.readline())
        self.ser.flush()
        self.ser.flushInput()
        self.ser.flushOutput()
        self.data = self.getData[2:][:-3]

        self.file = open(self.fileName, "a")
        self.file.write(self.data +",")
        self.file.close()

        self.xi = self.counter
        self.counter+=100
        self.yi = float(self.data)

        self.x.append(self.xi)
        self.y.append(self.yi)

        #self.ax.clear()
        #self.ax.plot()
        # self.ax.set_xlim([-20, 20])
        #xmin, xmax = self.ax.get_xlim()
        #ymin, ymax = self.ax.get_ylim()
        # xmin, xmax, ymin, ymax = plt.axis()
        self.mark = 'o'
        self.size = 3
        self.color = self.red
        self.ax.plot(self.xi, self.yi, color=self.color, marker=self.mark, markersize=self.size, linestyle='None')
        # self.ax.annotate('{:3.1f}%'.format(self.p_value * 100), 
        #                 xytext=(self.diff_measured + (xmax-self.diff_measured)*0.5, ymax//2), 
        #                 xy=(self.diff_measured, ymax//2), 
        #                 multialignment='right',
        #                 va='center',
        #                 color=self.red,
        #                 size='large',
        #                 arrowprops={'arrowstyle': '<|-', 
        #                             'lw': 2, 
        #                             'color': self.red, 
        #                             'shrinkA': 10})
        self.canvas.draw()
        self.after_id = self.after(100, self.start_readout)

    def stop_readout(self):
        """ stops readout of plot

        Returns: Nothing"""
        self.after_cancel(self.after_id)

    def ml(self):
        """uses ml to calc linear regression best fit for data set
        
        Returns: Nothing"""
        self.xml = np.array(self.x).reshape(-1,1) 
        self.yml = np.array(self.y).reshape(-1,1)       
        model = LinearRegression()
        

        poly = PolynomialFeatures(degree=5, include_bias=False)
        poly.fit(self.xml)
        self.x_poly = poly.transform(self.xml)

        #linear
        #model.fit(self.xml, self.yml)
        #self.y_pred = model.predict(self.xml)
        #self.ts = model.score(self.xml, self.y_pred)
        #self.ax.plot(self.x,self.y_pred, color=self.blue)
        #self.canvas.draw()

        #polynomial
        model.fit(self.x_poly,self.yml)
        self.y_pred = model.predict(self.x_poly)
        #self.polyscore = model.score(self.xml, self.y_pred)
        self.ax.plot(self.x,self.y_pred, color=self.green)
        self.canvas.draw()

root = tk.Tk()
root.resizable(False, False)
root.title("Chem-E-Car Readout")
TtestFrame(parent=root)
root.mainloop()