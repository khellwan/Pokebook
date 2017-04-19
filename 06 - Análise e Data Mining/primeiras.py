#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import Tkinter as tk



#Em python2 troque tkinter para Tkinter

try:
    conn = psycopg2.connect("dbname='1720465_Thiago' user='m0n0p0ly' host='200.134.10.32' password='#n0m0n3y#'")
except:
    print ("I am unable to connect to the database.")

TITLE_FONT = ("Helvetica", 18, "bold")

class Primeiras(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        
        label = tk.Label(self, text="Rating", font=TITLE_FONT)
        self.textfilmes = tk.Text(self, height=20, width=55, state="disabled")
        self.text2artistas = tk.Text(self, height=20, width=65, state="disabled")
        self.textfilmestop10 = tk.Text(self, height=7.5, width=30, state="disabled")
        self.text2artistastop10 = tk.Text(self, height=7.5, width=30, state="disabled")
        button_menu = tk.Button(self, text="Voltar para o menu principal",
                                    command=lambda: controller.show_frame("StartPage"))

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        #Rating de filmes top 10       
        try:
            cur.execute("SELECT filme, row_number() OVER (ORDER BY COUNT(filme) DESC) sid FROM curtefilme GROUP BY filme ORDER BY COUNT(filme) DESC LIMIT 10;")
        except Exception as e:
            print ("I can't SELECT from filmeTOP10")
            print (e)
        self.textfilmestop10.config(state="normal")
        self.textfilmestop10.delete(1.0, tk.END)

        rows = cur.fetchall()
        if (cur.rowcount == 0):
            self.textfilmestop10.insert(tk.END, "Não ha filmes.\n")
        else:
            self.textfilmestop10.insert(tk.END, ("Top10 filmes\n\n"))
            for row in rows:
                self.textfilmestop10.insert(tk.END, ("%s %s\n" % (row['sid'], row['filme'][27:-1])))

        #Rating de artistas top 10
        try:
            cur.execute("SELECT artista, row_number() OVER (ORDER BY COUNT(artista) DESC) sid FROM curtemusica GROUP BY artista ORDER BY COUNT(artista) DESC LIMIT 10;")
        except Exception as e:
            print ("I can't SELECT from artista")
            print (e)
        self.text2artistastop10.config(state="normal")
        self.text2artistastop10.delete(1.0, tk.END)
        rows = cur.fetchall()
        if (cur.rowcount == 0):
            self.text2artistastop10.insert(tk.END, "Não artistas.\n")
        else:
            self.text2artistastop10.insert(tk.END, ("Top10 artistas\n\n"))
            for row in rows:
                self.text2artistastop10.insert(tk.END, ("%s %s\n" % (row['sid'], row['artista'][30:])))

      
        #Filmes com maior rating     
        try:
            cur.execute("SELECT  stddev_samp(rating),avg(rating),filme FROM curtefilme GROUP BY filme HAVING (COUNT(filme)) > 2 ORDER BY avg(rating) DESC;")
        except Exception as e:
            print ("I can't SELECT from filme")
            print (e)
        self.textfilmes.config(state="normal")
        self.textfilmes.delete(1.0, tk.END)

        rows = cur.fetchall()
        if (cur.rowcount == 0):
            self.textfilmes.insert(tk.END, "Não há usuário cadastrado com essas informações.\n")
        else:
            self.textfilmes.insert(tk.END, ("Filmes com maior rating, suas notas e desvios padrões:\n\n"))
            for row in rows:
                self.textfilmes.insert(tk.END, ("Filme: %s     Nota: %s    Desvio:%s\n" % (row['filme'][27:-1], str(row['avg'])[:4],str(row['stddev_samp'])[:4], )))
        

        #Artistas com maior rating
        try:
            cur.execute("SELECT  stddev_samp(rating),avg(rating),artista FROM curtemusica GROUP BY artista HAVING (COUNT(artista)) > 2 ORDER BY avg(rating) DESC;")
        except Exception as e:
            print ("I can't SELECT from artista")
            print (e)
        self.text2artistas.config(state="normal")
        self.text2artistas.delete(1.0, tk.END)
        rows = cur.fetchall()
        if (cur.rowcount == 0):
            self.text2artistas.insert(tk.END, "Não há usuário cadastrado com essas informações.\n")
        else:
            self.text2artistas.insert(tk.END, "Artistas com maior rating, suas notas e desvios padrões:\n\n")
            for row in rows:
                self.text2artistas.insert(tk.END, ("Artista:%s%sNota:%s  Desvio:%s\n" % (row['artista'][30:]," "*(35-len(row['artista'][30:])), str(row['avg'])[:4], str(row['stddev_samp'])[:4],)))


        self.textfilmes.config(state="disabled")
        self.text2artistas.config(state="disabled")
        self.textfilmestop10.config(state="disabled")
        self.text2artistastop10.config(state="disabled")
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar2 = tk.Scrollbar(self)
        self.textfilmes.config(yscrollcommand=self.scrollbar.set)
        self.text2artistas.config(yscrollcommand=self.scrollbar2.set)


        button_menu.pack(side="bottom")
        self.scrollbar.config(command=self.textfilmes.yview)
        self.scrollbar2.config(command=self.text2artistas.yview)
        label.pack(side="top", fill="x", pady=10)
        self.scrollbar.pack(side="right", fill="y", expand=False)
        self.scrollbar2.pack(side="left", fill="y", expand=False)
        self.textfilmes.pack(side="right", fill="both", expand=True)
        self.text2artistas.pack(side="left", fill="both", expand=True)
        self.textfilmestop10.pack(side="top", fill="both", expand=True)
        self.text2artistastop10.pack(side="top", fill="both", expand=True)



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

#Final do Loop
