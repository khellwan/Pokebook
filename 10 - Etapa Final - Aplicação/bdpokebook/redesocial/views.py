from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files import File
from . import classes
import os, sys
import tensorflow as tf
import hashlib
from random import randint

		
def index(request):
	return render(request, 'index.html')
	
def friends(request):
	current_trainer = request.session['trainer_id']
	db_access = classes.acesso_banco()
	treinador = db_access.get_trainer(current_trainer)
	amigos = db_access.get_friends(current_trainer)
	sugestoes = db_access.get_friend_suggestions(current_trainer)
	return render(request, 'friends.html', {'treinador':treinador, 'amigos':amigos, 'sugestoes':sugestoes})

def pokemon(request):
	current_trainer = request.session['trainer_id']
	db_pokemon = classes.acesso_banco()
	treinador = db_pokemon.get_trainer(current_trainer)
	pokemons = db_pokemon.get_pokemons_by_trainer(current_trainer)
	#pokemon = db_pokemon.get_pokemons_by_trainer(id, especie, treinador, tipo, regiao, img, nivel, apelido)
	return render(request, 'pokemon.html', {'treinador':treinador, "pokemons" : pokemons})

def old_messages(request):
	db_msg = classes.acesso_banco()
	current_trainer = request.session['trainer_id']
	messages = db_msg.get_msg(current_trainer)
	return render(request, 'trainer.html', {'mensagens' : messages})
	
def post_message(request):
	db_msg = classes.acesso_banco()
	msg = request.POST.get('msg')
	data_atual = request.POST.get('data_atual')
	current_trainer = request.session['trainer_id']
	treinador = db_msg.get_trainer(current_trainer)
	message_id = randint(0, 99999)
	if (msg and msg != " "):
		db_msg.post_msg(message_id, current_trainer, msg)
	messages = db_msg.get_msg(current_trainer)
	return render(request, 'trainer.html', {'treinador' : treinador, 'mensagens':messages})
	
def delete_message(request):
	db_msg = classes.acesso_banco()
	msg = request.POST.get('id_msg')
	current_trainer = request.session['trainer_id']
	treinador = db_msg.get_trainer(current_trainer)
	messages = db_msg.get_msg(current_trainer)
	print("The message's ID is: ")
	print(msg)
	db_msg.delete_msg(msg)
	return render(request, 'trainer.html', {'treinador' : treinador, 'mensagens':messages})
	
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
	if (request.method=="GET" and request.GET.get('email')):
		current_trainer = request.GET.get('email')
		own_account = False
	else:
		current_trainer = request.session['trainer_id']
		own_account = True
	db_trainer = classes.acesso_banco()
	treinador = db_trainer.get_trainer(current_trainer)
	messages = db_trainer.get_msg(current_trainer)
	return render(request, 'trainer.html', {'treinador':treinador, 'mensagens':messages, 'own_account':own_account})

def form_signin(request):
	email = request.POST.get('email')
	md5_senha = hashlib.md5(request.POST.get('senha').encode('utf-8')).hexdigest()
	trainer = classes.acesso_banco()
	if trainer.login(email, md5_senha):
		request.session['trainer_id'] = email
		treinador = trainer.get_trainer(email)
		messages = trainer.get_msg(email)
		return render(request, 'trainer.html', {'treinador':treinador, 'mensagens':messages})
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
	trainer = classes.acesso_banco()
	trainer.create_trainer(email, nome, md5_senha, md5_confirma_senha, img_perfil, cidade)
	return render(request, 'index.html', {'sucesso': sucesso})
	
def form_signout(request):
	del request.session['trainer_id']
	print("Deslogou")
	return render(request, 'index.html')
	
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
