import pyodbc
from django.utils import timezone
import time



class acesso_banco():
	server = 'bispopokebookdb.database.windows.net'
	database = 'bispopokebookdb'
	username = 'thico10'
	password = 'LuThiWill9264'
#	server = 'bdutfpr.database.windows.net'
#	database = 'bdpokebook'
#	username = 'Willian1717553'
#	password = 'Bzxuyu_744'
	driver= '{ODBC Driver 13 for SQL Server}'
	cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()
	
	#fazer esse aqui ainda
	#def get_profile_pic():
		#cursor.execute("SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName FROM [SalesLT].[ProductCategory] pc JOIN [SalesLT].[Product] p ON pc.productcategoryid = p.productcategoryid")
		#row = cursor.fetchone()
		#while row:
	#		print str(row[0]) + " " + str(row[1])
	#		row = cursor.fetchone()
		#return
	"""	Acho q n vai precisar, mas ta ai se precisar
	def cnxn_connect():
		cnxn=pyodbc.connect('DRIVER='+acesso_banco.driver+';PORT=1433;SERVER='+acesso_banco.server+';PORT=1443;DATABASE='+acesso_banco.database+';UID='+acesso_banco.username+';PWD='+ acesso_banco.password)
		return cnxn
	"""
	def login(ref, email, senha):
		acesso_banco.cursor.execute("SELECT email FROM Treinador WHERE email= '{0}' AND senha='{1}';".format(email,senha))
		treinador = acesso_banco.cursor.fetchone()
		acesso_banco.cnxn.commit()
		if treinador:
			print("Logou com sucesso")
			return True
		else:
			print("O e-mail e/ou a senha esta/ao errados")
			return False
	
	def create_trainer(ref, email, nome, senha, confirma_senha, img_perfil, cidade):
		#print(email, nome, senha, confirma_senha, img_perfil, cidade, acesso_banco.username)
		if (senha != confirma_senha):
			print("Erro: as senhas sao diferentes.")
		else:
			acesso_banco.cursor.execute("INSERT INTO Treinador VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');" .format(email, nome, senha, img_perfil, cidade))
			print("Inserido com sucesso!")
			acesso_banco.cnxn.commit()
		return
	
	def get_pokemons_by_trainer(treinador):
		print("SELECT * FROM Pokemon WHERE treinador= '{0}'".format(treinador))
		acesso_banco.cursor.execute("SELECT * FROM Pokemon WHERE treinador= '{0}';".format(treinador))
		pokemon = acesso_banco.cursor.fetchone()
		acesso_banco.cnxn.commit()
		pokelist = []
		while pokemon:
			pokelist.append(pokemon)
			pokemon = acesso_banco.cursor.fetchone()
		return pokelist
		
	def get_trainer(ref, current_trainer):
		acesso_banco.cursor.execute("SELECT * FROM Treinador WHERE email = '{0}';".format(current_trainer))
		row = acesso_banco.cursor.fetchone()
		treinador = Treinador(row[0],row[1],row[3],row[4])
		acesso_banco.cnxn.commit()
		return treinador
	
	def get_trainer_pic(ref, current_trainer):
		acesso_banco.cursor.execute("SELECT img_perfil FROM Treinador WHERE email = '{0}';".format(current_trainer))
		row = acesso_banco.cursor.fetchone()
		profile_pic = row[0]
		acesso_banco.cnxn.commit()
		return profile_pic
		
	def get_trainer_name(ref, current_trainer):
		acesso_banco.cursor.execute("SELECT nome FROM Treinador WHERE email = '{0}';".format(current_trainer))
		row = acesso_banco.cursor.fetchone()
		trainer_name = row[0]
		acesso_banco.cnxn.commit()
		return trainer_name
		
	def get_msg(ref, current_trainer):
		acesso_banco.cursor.execute("SELECT * FROM Mensagem WHERE login_treinador = '{0}' ORDER BY data_postagem DESC;".format(current_trainer))
		mensagem = acesso_banco.cursor.fetchall()
		acesso_banco.cnxn.commit()
		msg_list = []
		for m in mensagem:
			msg = Mensagem(m[0],m[1],m[2],m[3])
			msg_list.append(msg)
		return msg_list
		
		
	def get_data_msg(ref, current_trainer):
		acesso_banco.cursor.execute("SELECT data FROM Mensagem WHERE login_treinador = {0};".format(current_trainer))
		mensagem = acesso_banco.cursor.fetchone()
		acesso_banco.cnxn.commit()
		datas = []
		while mensagem:
			datas.append(data[0])
			data = acesso_banco.cursor.fetchone()
		return data_list
		
	def post_msg(ref, id_msg, login_treinador, conteudo):
		now = timezone.now()
		data = now.strftime('%Y-%m-%d %H:%M:%S')
		print("INSERT INTO Mensagem VALUES ('{0}', '{1}', '{2}', '{3}');".format(id_msg, login_treinador, conteudo, data))
		acesso_banco.cursor.execute("INSERT INTO Mensagem VALUES ('{0}', '{1}', '{2}', '{3}');".format(id_msg, login_treinador, conteudo, data))
		acesso_banco.cnxn.commit()
		print("Inserido com sucesso!")
		return
		
	
class Pokemon:
	def __init__(self, apelido, especie, tipo, regiao, estado_evolucao, img, nivel, treinador):
		self.apelido = apelido
		self.especie = especie
		self.tipo = tipo
		self.regiao = regiao
		self.estado_evolucao = estado_evolucao
		self.img = img
		self.nivel = nivel
		self.treinador = treinador

class Treinador:
	def __init__(self, login, nome, img_perfil, cidade):
		self.login=login
		self.nome=nome
		self.img_perfil=img_perfil
		self.cidade=cidade
		
class Mensagem:
	def __init__(self, id_msg, login_treinador, conteudo, data_postagem):
		self.id_msg=id_msg
		self.conteudo=conteudo
		self.login_treinador=login_treinador
		self.data_postagem=data_postagem