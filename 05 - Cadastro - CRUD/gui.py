#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import os
import urllib
import tkinter as tk

#Em python2 troque tkinter para Tkinter



#Acesso ao banco de dados
try:
        conn = psycopg2.connect("dbname='1720465_Thiago' user='m0n0p0ly' host='200.134.10.32' password='#n0m0n3y#'")
except:
        print ("I am unable to connect to the database.")

cur = conn.cursor()

#Acesso ao banco de dados

#Inicio do Loop
TITLE_FONT = ("Helvetica", 18, "bold")

class SampleApp(tk.Tk):

        def __init__(self, *args, **kwargs):
                tk.Tk.__init__(self, *args, **kwargs)
                self.wm_title("Interface CRUD")
        
                # the container is where we'll stack a bunch of frames
                # on top of each other, then the one we want visible
                # will be raised above the others
                container = tk.Frame(self)
                container.pack(side="top", fill="both", expand=True)
                container.grid_rowconfigure(0, weight=1)
                container.grid_columnconfigure(0, weight=1)

                self.frames = {}
                for F in (StartPage, Listar, Cadastrar, Atualizar, Deletar):
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


class StartPage(tk.Frame):

        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
        
                self.controller = controller
                
                label = tk.Label(self, text="Interface CRUD", font=TITLE_FONT)        
                button1 = tk.Button(self, text="Listar", command=lambda: controller.show_frame("Listar"))
                button2 = tk.Button(self, text="Cadastrar", command=lambda: controller.show_frame("Cadastrar"))

                label.pack(side="top", fill="x", pady=10)
                button1.pack()
                button2.pack()

class Listar(tk.Frame):
        
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                self.controller = controller
                
                label = tk.Label(self, text="Listagem de Pessoas", font=TITLE_FONT)
                info = tk.Label(self, text="Lista de pessoas")
                self.text = tk.Text(self, height=15, width=150, state="disabled")
                button_menu = tk.Button(self, text="Voltar para o menu principal",
                                                   command=lambda: controller.show_frame("StartPage"))
                button_atualizar = tk.Button(self, text="Atualizar Usuário",
                                             command=lambda: controller.show_frame("Atualizar"))
                button_deletar = tk.Button(self, text="Deletar Usuário",
                                             command=lambda: controller.show_frame("Deletar"))

                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)                
                try:
                        cur.execute("SELECT * FROM pessoa")
                except Exception as e:
                        print ("I can't SELECT from pessoa")
                        print (e)
                self.text.config(state="normal")
                self.text.delete(1.0, tk.END)
                rows = cur.fetchall()
                if (cur.rowcount == 0):
                        self.text.insert(tk.END, "Não há usuário cadastrado com essas informações.\n")
                else:		
                        for row in rows:	
                                self.text.insert(tk.END, ("Login: '%s' Nome: '%s' Cidade Natal: '%s'\n" % (row['login'], row['nome_completo'], row['cidade_natal'])))
                
                self.text.config(state="disabled")

                self.scrollbar = tk.Scrollbar(self)

                self.text.config(yscrollcommand=self.scrollbar.set)
                self.scrollbar.config(command=self.text.yview)
                
                label.pack(side="top", fill="x", pady=10)
                info.pack()
                self.scrollbar.pack(side="right", fill="y", expand=False)
                self.text.pack(side="right", fill="both", expand=True)

                button_atualizar.pack()
                button_deletar.pack()
                button_menu.pack(pady=10)

class Cadastrar(tk.Frame):
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                self.controller = controller
                
                label = tk.Label(self, text="Cadastro", font=TITLE_FONT)
                info = tk.Label(self, text="Insira os dados do usuário que deseja cadastrar")
                button_menu = tk.Button(self, text="Voltar para o menu principal", command=lambda: controller.show_frame("StartPage"))
                button_usuario = tk.Button(self, text="Cadastrar usuário", command=lambda: self.insert_db())
                button_conhecido = tk.Button(self, text="Cadastrar conhecido", command=lambda: self.insert_conhecido())
                label_login = tk.Label(self, text="Login")
                label_nome = tk.Label(self, text="Nome")
                label_cidade = tk.Label(self, text="Cidade Natal")
                info2 = tk.Label(self, text="Insira o login de quem conhece e de quem é conhecido")
                label_login_conhecedor = tk.Label(self, text="Login de quem conhece")
                label_login_conhecido = tk.Label(self, text="Login de quem é conhecido")
                self.entry_login = tk.Entry(self, bd = 5)	   
                self.entry_nome = tk.Entry(self, bd = 5)
                self.entry_cidade = tk.Entry(self, bd = 5)
                self.entry_login_conhecedor = tk.Entry(self, bd = 5)
                self.entry_login_conhecido = tk.Entry(self, bd = 5)
                self.text = tk.Text(self, height=2, width=60, state="disabled")
                
                label.pack(side="top", fill="x", pady=10)
                info.pack()
                label_login.pack()
                self.entry_login.pack()
                label_nome.pack()
                self.entry_nome.pack()
                label_cidade.pack()
                self.entry_cidade.pack()
                button_usuario.pack(pady=5)
                info2.pack()
                label_login_conhecedor.pack()
                self.entry_login_conhecedor.pack()
                label_login_conhecido.pack()
                self.entry_login_conhecido.pack()
                button_conhecido.pack()
                self.text.pack(pady=10, padx=5)
                button_menu.pack()

        def insert_db(self):
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                self.text.config(state="normal")
                self.text.delete(1.0, tk.END)
                login_cabra = self.entry_login.get()
                if login_cabra == "":
                        login_cabra = None
                try:
                                cur.execute("INSERT INTO pessoa VALUES (%s,%s,%s);", (self.entry_cidade.get(), self.entry_nome.get(), login_cabra))
                                self.text.insert(tk.END, "Usuário cadastrado com sucesso.\n")
                except Exception as e:
                        print ("I can't INSERT INTO pessoa")
                        print (e)
                        self.text.insert(tk.END, "Não foi possível cadastrar o usuário.\n")
                conn.commit()
                self.text.config(state="disabled")
        def insert_conhecido(self):
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                self.text.config(state="normal")
                self.text.delete(1.0, tk.END)
                try:
                        cur.execute("INSERT INTO registra VALUES (%s,%s);", (self.entry_login_conhecedor.get(), self.entry_login_conhecido.get()))
                        self.text.insert(tk.END, "Relacionamento cadastrado com sucesso.\n")
                except Exception as e:
                        print ("I can't INSERT INTO pessoa")
                        print (e)
                        self.text.insert(tk.END, "Não foi possível cadastrar o usuário.\n")
                conn.commit()
                self.text.config(state="disabled")
                

class Atualizar(tk.Frame):

        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                self.controller = controller
                
                label = tk.Label(self, text="Atualizar dados", font=TITLE_FONT)
                info = tk.Label(self, text="Insira os dados do usuário que se deseja atualizar e os novos dados")
                button_menu = tk.Button(self, text="Voltar para o menu principal",
                                                   command=lambda: controller.show_frame("StartPage"))
                button_send = tk.Button(self, text="Atualizar usuário", command=lambda: self.update_db())
                self.text = tk.Text(self, height=2, width=60, state="disabled")
                label_old_login = tk.Label(self, text="Login Antigo")
                label_old_nome = tk.Label(self, text="Nome Antigo")
                label_old_cidade = tk.Label(self, text="Cidade Natal Antiga")
                self.entry_old_login = tk.Entry(self, bd = 5)
                self.entry_old_nome = tk.Entry(self, bd = 5)
                self.entry_old_cidade = tk.Entry(self, bd = 5)
                label_new_login = tk.Label(self, text="Login Novo")
                label_new_nome = tk.Label(self, text="Nome Novo")
                label_new_cidade = tk.Label(self, text="Cidade Natal Nova")
                self.entry_new_login = tk.Entry(self, bd = 5)
                self.entry_new_nome = tk.Entry(self, bd = 5)
                self.entry_new_cidade = tk.Entry(self, bd = 5)
                
                label.pack(side="top", fill="x", pady=10)
                info.pack()
                label_old_login.pack()
                self.entry_old_login.pack()
                label_old_nome.pack()
                self.entry_old_nome.pack()
                label_old_cidade.pack()
                self.entry_old_cidade.pack()
                label_new_login.pack()
                self.entry_new_login.pack()
                label_new_nome.pack()
                self.entry_new_nome.pack()
                label_new_cidade.pack()
                self.entry_new_cidade.pack()
                button_send.pack(pady=5)
                self.text.pack(pady=10, padx=5)
                button_menu.pack()

        def update_db(self):
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                self.text.config(state="normal")
                self.text.delete(1.0, tk.END)
                data = [self.entry_new_login.get(), self.entry_new_nome.get(), self.entry_new_cidade.get(), self.entry_old_login.get(), self.entry_old_nome.get(), self.entry_old_cidade.get()]
                if data[0] == "":
                        data[0]=data[3]
                if data[1] == "":
                        data[1]=data[4]
                if data[2] == "":
                        data[2]=data[5]
                try:
                        cur.execute("UPDATE pessoa SET login =%s, nome_completo =%s, cidade_natal =%s WHERE login =%s AND nome_completo =%s AND cidade_natal =%s;", (data[0], data[1], data[2], self.entry_old_login.get(), self.entry_old_nome.get(), self.entry_old_cidade.get()))
                        self.text.insert(tk.END, "Usuário atualizado com sucesso.\n")
                except Exception as e:
                        print ("I can't UPDATE pessoa")
                        print (e)
                        self.text.insert(tk.END, "Não foi possível atualizar o usuário.\n")
                conn.commit()
                self.text.config(state="disabled")


class Deletar(tk.Frame):

        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                self.controller = controller

                label = tk.Label(self, text="Deletar dados", font=TITLE_FONT)
                info = tk.Label(self, text="Insira os dados do usuário que se deseja deletar")
                button_menu = tk.Button(self, text="Voltar para o menu principal", command=lambda: controller.show_frame("StartPage"))
                button_send = tk.Button(self, text="Deletar usuário", command=lambda: self.delete_db())
                label_login = tk.Label(self, text="Login")
                self.entry_login = tk.Entry(self, bd = 5)
                self.text = tk.Text(self, height=10, width=60, state="disabled")

                label.pack(side="top", fill="x", pady=10)
                info.pack(fill="x", pady=5)
                label_login.pack()
                self.entry_login.pack()
                button_send.pack(pady=5)
                self.text.pack(pady=10, padx=5)
                button_menu.pack()      
                
        def delete_db(self):
                cur = conn.cursor()
                self.text.config(state="normal")
                self.text.delete(1.0, tk.END)
                try:
                        cur.execute("DELETE FROM pessoa WHERE login ='%s';" % (self.entry_login.get()))
                        if cur.rowcount != 0:
                                self.text.insert(tk.END, "Usuário deletado com sucesso.\n")
                        else:
                                self.text.insert(tk.END, "Não há usuário cadastrado com esse login.\n")
                except Exception as e:
                        print ("I can't Delete pessoa")
                        print (e)
                        self.text.insert(tk.END, "Não foi possível deletar o usuário.\n")
                self.text.config(state="disabled")
                conn.commit()
        

if __name__ == "__main__":
        app = SampleApp()
        app.mainloop()

#Final do Loop
