#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
import psycopg2
import psycopg2.extras


#Em python2 troque tkinter para Tkinter


try:
        conn = psycopg2.connect("dbname='1720465_Thiago' user='m0n0p0ly' host='200.134.10.32' password='#n0m0n3y#'")
except:
        print ("I am unable to connect to the database.")

cur = conn.cursor()

TITLE_FONT = ("Helvetica", 18, "bold")

class Extras(tk.Frame):
        
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		
		label = tk.Label(self, text="Extras", font=TITLE_FONT)
		info = tk.Label(self, text="Pessoas que mais compartilham artistas curtidos               -- Pessoa que mais possui conhecido")
		self.text = tk.Text(self, height=15, width=60, state="disabled")  
		button_menu = tk.Button(self, text="Voltar para o menu principal",
		                                   command=lambda: controller.show_frame("StartPage"))                         
	

		label.pack(side="top", fill="x", pady=10)
		info.pack(side="top", fill="x")
		button_menu.pack(side="bottom")

		self.text.pack(side="right", fill="both", expand=True)
		
		self.extras_db()
		

	def extras_db(self):
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                self.text.config(state="normal")
                self.text.delete(1.0, tk.END)

		''' Pessoas que mais compartilham curtidas de musicas ''' 

		cur.execute("SELECT t1.curtidor AS curtidor1,t2.curtidor AS curtidor2,count(*) AS N_State FROM curteMusica t1, curteMusica t2, conheceNormalizada C WHERE t2.artista = t1.artista AND t2.curtidor != t1.curtidor AND C.conhecedor = t1.curtidor AND C.conhecido = t2.curtidor GROUP BY t1.curtidor,t2.curtidor ORDER BY N_State DESC")
		
		rows = cur.fetchall()
		maior = 0
		curtidores1 = []
		curtidores2 = []
		for row in rows:
			if row['n_state'] >= maior:
				maior = row['n_state']			
				if (row['curtidor1'] not in curtidores2) and (row['curtidor2'] not in curtidores1):						
					self.text.insert(tk.END, ("Os conhecidos que mais compartilham número de artistas são '%s' e '%s' que compartilham '%s' artistas.\n\n" % (row['curtidor1'].replace("http://utfpr.edu.br/CSB30/2017/1/", ""), row['curtidor2'].replace("http://utfpr.edu.br/CSB30/2017/1/", ""), row['n_state'])))
					curtidores1.append(row['curtidor1'])
					curtidores2.append(row['curtidor2'])
		
		''' Pessoas que mais possuem conhecidos ''' 
		maior = 0
		cur.execute("SELECT login_registrador AS Conhecedor, count(*) AS n_state FROM registra GROUP BY Conhecedor ORDER BY n_state DESC")
		conn.commit()	
		cur.execute("SELECT * FROM ConheceNormalizada")
		rows = cur.fetchall()
		for row in rows:
			if row['n_state'] >= maior:
				maior = row['n_state']	
				self.text.insert(tk.END, ("A pessoa que mais possui conhecido é '%s' e possui '%s' conhecidos. " % (row['curtidor1'].replace("http://utfpr.edu.br/CSB30/2017/1/", ""), row['n_state'])))

                self.text.config(state="disabled")		

