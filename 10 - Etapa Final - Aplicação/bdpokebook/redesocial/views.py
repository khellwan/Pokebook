from django.shortcuts import render
from django.http import HttpResponseRedirect
import pyodbc
import hashlib

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
		
	def create_trainer(ref, email, nome, senha, confirma_senha, img_perfil, cidade) :
		#print(email, nome, senha, confirma_senha, img_perfil, cidade, acesso_banco.username)
		if (senha != confirma_senha):
			print("Erro: as senhas são diferentes.")
		else:
			print("INSERT INTO Trainer VALUES ({0}, {1}, MD5({2}), {3}, {4})" .format(email, nome, senha, img_perfil, cidade))
			acesso_banco.cursor.execute("INSERT INTO Treinador VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')" .format(email, nome, senha, img_perfil, cidade))
			print("Inserido com sucesso!")
			acesso_banco.cnxn.commit()
			acesso_banco.cnxn.close()
		return

def index(request):
	return render(request, 'index.html')
	
def friends(request):
	return render(request, 'friends.html')

def photos(request):
	return render(request, 'photos.html')

def pokemon(request):
	return render(request, 'pokemon.html')

def quest(request):
	return render(request, 'quest.html')

def sign_up(request):
	return render(request, 'sign-up.html')

def trainer(request):
	link="http://s2.quickmeme.com/img/7a/7a815ba5e4b102a9250a8773652d8278304583207d8e944782d8e2a6cfa580ef.jpg"
	return render(request, 'trainer.html', {'link' : link})	

def submit(request):
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
	

# Create your views here.
