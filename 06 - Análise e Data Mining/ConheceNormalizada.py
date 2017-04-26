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

class ConheceNormalizada(tk.Frame):
        
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		
		label = tk.Label(self, text="Relacionamentos", font=TITLE_FONT)
		info = tk.Label(self, text="View dos Relacionamentos                   --               Filmes em Comum               --                   Conhecidos de Conhecidos")
		self.text_view = tk.Text(self, height=15, width=60, state="disabled")
		self.text_share = tk.Text(self, height=15, width=60, state="disabled")
		self.text_amount = tk.Text(self, height=15, width=60, state="disabled")    
		button_menu = tk.Button(self, text="Voltar para o menu principal",
		                                   command=lambda: controller.show_frame("StartPage"))                         
		self.scrollbar_view = tk.Scrollbar(self)
		self.scrollbar_share = tk.Scrollbar(self)
		self.scrollbar_amount = tk.Scrollbar(self)

		self.text_view.config(yscrollcommand=self.scrollbar_view.set)
		self.scrollbar_view.config(command=self.text_view.yview)

		self.text_share.config(yscrollcommand=self.scrollbar_share.set)
		self.scrollbar_share.config(command=self.text_share.yview)

		self.text_amount.config(yscrollcommand=self.scrollbar_amount.set)
		self.scrollbar_amount.config(command=self.text_amount.yview)		

		label.pack(side="top", fill="x", pady=10)
		info.pack(side="top", fill="x")
		button_menu.pack(side="bottom")

		
		self.scrollbar_amount.pack(side="right", fill="y", expand=False)
		self.text_amount.pack(side="right", fill="both", expand=True)

		self.scrollbar_share.pack(side="right", fill="y", expand=False)
		self.text_share.pack(side="right", fill="both", expand=True)

		self.scrollbar_view.pack(side="right", fill="y", expand=False)
		self.text_view.pack(side="right", fill="both", expand=True)
		
		self.view_db()
		

	def view_db(self):
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                self.text_view.config(state="normal")
                self.text_view.delete(1.0, tk.END)
		self.text_share.config(state="normal")
                self.text_share.delete(1.0, tk.END)
		self.text_amount.config(state="normal")
                self.text_amount.delete(1.0, tk.END)

		maior = 0
		curtidores1 = []
		curtidores2 = []
	         
		''' Criação da View '''         
       
		try:
			try:			
				cur.execute("DROP VIEW ConheceNormalizada")
			except:
				print ("View ainda não existe, mas será criada.")

			conn.commit()                     
			cur.execute("CREATE VIEW ConheceNormalizada AS SELECT login_registrador AS Conhecedor, login_registrado AS Conhecido FROM registra UNION SELECT login_registrado AS Conhecedor, login_registrador AS Conhecido FROM registra ORDER BY Conhecedor, Conhecido")
			conn.commit()	
			cur.execute("SELECT * FROM ConheceNormalizada")
                except Exception as e:
                        print ("I can't CREATE VIEW")
                        print (e)
                        self.text_view.insert(tk.END, "Não foi possível criar uma view.\n")

		rows = cur.fetchall()
                if (cur.rowcount == 0):
                        self.text_view.insert(tk.END, "Não há relacionamento cadastrado com essas informações.\n")
                else:		
                        for row in rows:
                                self.text_view.insert(tk.END, ("'%s' CONHECE '%s'\n" % (row['conhecedor'].replace("http://utfpr.edu.br/CSB30/2017/1/", ""), row['conhecido'].replace("http://utfpr.edu.br/CSB30/2017/1/", ""))))

		''' Pessoas que mais compartilham curtidas de filmes ''' 

		cur.execute("SELECT t1.curtidor AS curtidor1,t2.curtidor AS curtidor2,count(*) AS N_State FROM curteFilme t1, curteFilme t2, conheceNormalizada C WHERE t2.filme = t1.filme AND t2.curtidor != t1.curtidor AND C.conhecedor = t1.curtidor AND C.conhecido = t2.curtidor GROUP BY t1.curtidor,t2.curtidor ORDER BY N_State DESC")
		
		rows = cur.fetchall()

		for row in rows:
			if row['n_state'] >= maior:
				maior = row['n_state']			
				if (row['curtidor1'] not in curtidores2) and (row['curtidor2'] not in curtidores1):						
					self.text_share.insert(tk.END, ("Os conhecidos que mais compartilham número de filmes são '%s' e '%s' que compartilham '%s' filmes.\n\n" % (row['curtidor1'].replace("http://utfpr.edu.br/CSB30/2017/1/", ""), row['curtidor2'].replace("http://utfpr.edu.br/CSB30/2017/1/", ""), row['n_state'])))
					curtidores1.append(row['curtidor1'])
					curtidores2.append(row['curtidor2'])

		''' Conhecidos dos conhecidos ''' 

		cur.execute("SELECT C.conhecedor, count(*) AS n_conhecidos FROM (SELECT Conhecedor, Conhecido FROM ConheceNormalizada ORDER BY Conhecedor) C, ConheceNormalizada D WHERE D.Conhecedor = C.Conhecido GROUP BY C.Conhecedor ORDER BY C.Conhecedor")
		rows = cur.fetchall()
		for row in rows:
			self.text_amount.insert(tk.END, ("Os conhecidos de '%s' conhecem '%s' pessoas. \n\n" % (row['conhecedor'].replace("http://utfpr.edu.br/CSB30/2017/1/", ""), row['n_conhecidos'])))
		
		
                self.text_view.config(state="disabled")
		self.text_share.config(state="disabled")
		self.text_amount.config(state="disabled")

