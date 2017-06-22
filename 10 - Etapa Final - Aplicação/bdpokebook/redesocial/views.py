from django.shortcuts import render
from django.http import HttpResponseRedirect
import pyodbc
import hashlib

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files import File
import os, sys
import tensorflow as tf

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
		acesso_banco.cursor.execute("SELECT email FROM Treinador WHERE email= '{0}' AND senha='{1}'".format(email,senha))
		treinador = acesso_banco.cursor.fetchone()
		acesso_banco.cnxn.commit()
		if treinador:
			print("Logou com sucesso")
			return True
		else:
			print("O e-mail ou a senha estão errados")
			return False
	
	def create_trainer(ref, email, nome, senha, confirma_senha, img_perfil, cidade):
		#print(email, nome, senha, confirma_senha, img_perfil, cidade, acesso_banco.username)
		if (senha != confirma_senha):
			print("Erro: as senhas são diferentes.")
		else:
			print("INSERT INTO Trainer VALUES ({0}, {1}, MD5({2}), {3}, {4})" .format(email, nome, senha, img_perfil, cidade))
			acesso_banco.cursor.execute("INSERT INTO Treinador VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')" .format(email, nome, senha, img_perfil, cidade))
			print("Inserido com sucesso!")
			acesso_banco.cnxn.commit()
		return
	
	def get_pokemons_by_trainer(treinador):
		print("SELECT * FROM Pokemon WHERE treinador= '{0}'".format(treinador))
		acesso_banco.cursor.execute("SELECT * FROM Pokemon WHERE treinador= '{0}'".format(treinador))
		acesso_banco.cnxn.commit()
		pokemon = acesso_banco.cursor.fetchone()
		pokelist = []
		while pokemon:
			pokelist.append(pokemon)
			pokemon = acesso_banco.cursor.fetchone()
		return pokelist

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

		
def index(request):
	return render(request, 'index.html')
	
def friends(request):
	return render(request, 'friends.html')

def photos(request):
	return render(request, 'photos.html')

def pokemon(request):
	#trainer = request.session['trainer_id'] tem que definir isso quando o cara logar
	#pokelist = get_pokemons_by_trainer()
	pokelist = [] #temporario enquanto n tem as tabelas
	for i in range(6):
		apelido = "pokemon" + str(i)
		especie = "especie" + str(i)
		tipo = "fire"
		regiao = "inacio"
		estado_evolucao = i
		img = "img" + str(i) + ".com"
		nivel = i
		treinador = "ash ketchum"
		pokemon = Pokemon(apelido, especie, tipo, regiao, estado_evolucao, img, nivel, treinador)
		pokelist.append(pokemon)
	return render(request, 'pokemon.html', {"range" : range(6), "pokemon" : pokelist})

	
def quest(request):
	if request.method == 'POST' and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		imagem = open(uploaded_file_url, 'rb').read()
		texto = Classify(imagem)
		return render(request, 'quest.html', {
			'uploaded_file_url': uploaded_file_url, 'texto': texto
		})
	return render(request, 'quest.html')

def sign_up(request):
	return render(request, 'sign-up.html')

def trainer(request):
	link="http://s2.quickmeme.com/img/7a/7a815ba5e4b102a9250a8773652d8278304583207d8e944782d8e2a6cfa580ef.jpg"
	return render(request, 'trainer.html', {'link' : link})	

def form_signin(request):
	email = request.POST.get('email')
	md5_senha = hashlib.md5(request.POST.get('senha').encode('utf-8')).hexdigest()
	trainer = acesso_banco()
	if trainer.login(email, md5_senha):
		request.session['trainer_id'] = email
		return render(request, 'trainer.html')
	else:
		return render(request, 'index.html', {'erro' : "O e-mail ou a senha estão errados"})

def form_signup(request):
	email = request.POST.get('email')
	nome = request.POST.get('nome')
	md5_senha = hashlib.md5(request.POST.get('senha').encode('utf-8')).hexdigest()
	md5_confirma_senha = hashlib.md5(request.POST.get('confirma_senha').encode('utf-8')).hexdigest()
	img_perfil = request.POST.get('img_perfil')
	cidade = request.POST.get('cidade')
	sucesso = "Registrado com Sucesso!"
	#print(cidade)
	#print(email)
	#print(nome)
	trainer = acesso_banco()
	#print(email, nome, md5_senha, md5_confirma_senha, img_perfil, cidade)
	trainer.create_trainer(email, nome, md5_senha, md5_confirma_senha, img_perfil, cidade)
	return render(request, 'index.html', {'sucesso': sucesso})
	
def Classify(image_data):
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

	# Loads label file, strips off carriage return
	label_lines = [line.rstrip() for line 
					   in open('redesocial/retrained_labels.txt', "rb")]

	# Unpersists graph from file
	with open('redesocial/retrained_graph.pb', "rb") as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		tf.import_graph_def(graph_def, name='')

	with tf.Session() as sess:
		# Feed the image_data as input to the graph and get first prediction
		softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
		
		predictions = sess.run(softmax_tensor, \
				 {'DecodeJpeg/contents:0': image_data})
		
		# Sort to show labels of first prediction in order of confidence
		top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
		
		for node_id in top_k:
			human_string = label_lines[node_id]
			score = predictions[0][node_id]
			return(human_string)
			print('%s (score = %.5f)' % (human_string, score))
	return(label_lines[0])

# Create your views here.
