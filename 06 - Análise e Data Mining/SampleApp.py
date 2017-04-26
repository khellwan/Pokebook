#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
from StartPage import StartPage
from ConheceNormalizada import ConheceNormalizada
from graficos import Graficos
from primeiras import Primeiras
from extras import Extras
import psycopg2
import psycopg2.extras

#Em python2 troque tkinter para Tkinter

#Acesso ao banco de dados
try:
        conn = psycopg2.connect("dbname='1720465_Thiago' user='m0n0p0ly' host='200.134.10.32' password='#n0m0n3y#'")
except:
        print ("I am unable to connect to the database.")

cur = conn.cursor()


TITLE_FONT = ("Helvetica", 18, "bold")

class SampleApp(tk.Tk):

        def __init__(self, *args, **kwargs):
	        tk.Tk.__init__(self, *args, **kwargs)
		self.wm_title("Analise e Data Mining")

		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for F in (StartPage, Primeiras, Graficos, ConheceNormalizada, Extras):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame

			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("StartPage")

        def show_frame(self, page_name):
                '''Show a frame for the given page name'''
                frame = self.frames[page_name]
                frame.tkraise()

