#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
from ConheceNormalizada import ConheceNormalizada

#Em python2 troque tkinter para Tkinter

TITLE_FONT = ("Helvetica", 18, "bold")

class StartPage(tk.Frame):

        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
        
                self.controller = controller
                
                label = tk.Label(self, text="Análise e Data Mining", font=TITLE_FONT)        
                button1 = tk.Button(self, text="View", command=lambda: controller.show_frame("ConheceNormalizada"))
		button2 = tk.Button(self, text="Rating", command=lambda: controller.show_frame("Primeiras"))
		button3 = tk.Button(self, text="Graphics", command=lambda: controller.show_frame("Graficos"))
		button4 = tk.Button(self, text="Extras", command=lambda: controller.show_frame("Extras"))

                label.pack(side="top", fill="x", pady=10)
		button2.pack()                
		button1.pack()
		button3.pack()
		button4.pack()

