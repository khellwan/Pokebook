#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import Tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

#Em python2 troque tkinter para Tkinter



#Acesso ao banco de dados
try:
        conn = psycopg2.connect("dbname='1720465_Thiago' user='m0n0p0ly' host='200.134.10.32' password='#n0m0n3y#'")
except:
        print ("I am unable to connect to the database.")

cur = conn.cursor()

TITLE_FONT = ("Helvetica", 18, "bold")


class Graficos(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)        
        self.controller = controller

        label = tk.Label(self, text="Gráficos", font=TITLE_FONT)
        label.pack(side=tk.TOP, fill="x", pady=10)

        button_menu = tk.Button(self, text="Voltar para o menu principal",
                                                   command=lambda: controller.show_frame("StartPage"))
        button_menu.pack(pady=5)
        
        #Começa a processar o banco para plotar os gráficos
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        #Conta pessoas
        try:
            cur.execute("SELECT * FROM pessoa")
        except Exception as e:
            print ("I can't SELECT from pessoa")
            print (e)
        d_pessoa = {}
        rows = cur.fetchall()
        for row in rows:
            d_pessoa[row['login']]=0

        #Conta filmes
        try:
            cur.execute("SELECT * FROM filme")
        except Exception as e:
            print ("I can't SELECT from filme")
            print (e)
        d_filme = {}
        rows = cur.fetchall()
        for row in rows:
            d_filme[row['id']]=0        
        
        #Processa o relacionamento de Curtir Filme
        try:
            cur.execute("SELECT * FROM curtefilme")
        except Exception as e:
            print ("I can't SELECT from curtefilme")
            print (e)
        
        rows=cur.fetchall()
        for row in rows:
            d_pessoa[row['curtidor']] += 1
            d_filme[row['filme']] += 1
        
        #Processa os dados para os plots
        plot_filme = [0]*(len(d_pessoa)+1) #Filme curtido por x pessoas
        plot_pessoa = [0]*(len(d_filme)+1) #Pessoa curte x filmes
        for n_pessoas in d_filme.values():
            plot_filme[n_pessoas]+=1
        for n_filmes in d_pessoa.values():
            plot_pessoa[n_filmes]+=1
        #Faz os plots
        f = Figure(figsize=(7,9), dpi=60)
        a_pessoa = f.add_subplot(211)
        a_pessoa.set_title('Pessoa curte x filmes')
        a_pessoa.set_xlabel('Filmes', fontsize=8)
        a_pessoa.set_ylabel('N pessoas', fontsize=8)
        a_pessoa.plot(range(len(d_filme)+1),plot_pessoa)

        canvas_pessoa = FigureCanvasTkAgg(f, self)
        canvas_pessoa.draw()
        canvas_pessoa.get_tk_widget().pack(padx=10)

        toolbar_pessoa = NavigationToolbar2TkAgg(canvas_pessoa, self)
        toolbar_pessoa.update()
        canvas_pessoa._tkcanvas.pack(padx=10)

        a_filme = f.add_subplot(212)
        a_filme.set_title('Filme foi curtido por x pessoas')
        a_filme.set_xlabel('Pessoas', fontsize=8)
        a_filme.set_ylabel('N filmes', fontsize=8)
        a_filme.plot(range(len(d_pessoa)+1),plot_filme)

