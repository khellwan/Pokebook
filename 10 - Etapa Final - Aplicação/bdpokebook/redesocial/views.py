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
	return render(request, 'friends.html')


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

def old_messages(request):
	db_msg = classes.acesso_banco()
	current_trainer = request.session['trainer_id']
	messages = db_msg.get_msg(current_trainer)
	datas = db_msg.get_data_msg(current_trainer)
	for msg in messages:
		conteudo = messages[msg]
		data_msg = datas[msg]
	return render(request, 'trainer.html', {'msg': msg, 'messages' : messages, 'conteudo' : conteudo, 'current_trainer' : current_trainer, 'data_msg' : data_msg})
	
def post_message(request):
	db_msg = classes.acesso_banco()
	msg = request.POST.get('msg')
	data_atual = request.POST.get('data_atual')
	current_trainer = request.session['trainer_id']
	profile_pic = request.session['profile_pic']
	trainer_name = request.session['trainer_name']
	message_id = randint(0, 99999)
	if (msg != "None"):
		db_msg.post_msg(message_id, current_trainer, msg, data_atual)
	return render(request, 'trainer.html', {'profile_pic' : profile_pic, 'trainer_name' : trainer_name})
	
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
	current_trainer = request.session['trainer_id']
	db_trainer = classes.acesso_banco()
	profile_pic = db_trainer.get_trainer_pic(current_trainer)
	request.session['profile_pic'] = profile_pic
	trainer_name = db_trainer.get_trainer_name(current_trainer)
	request.session['trainer_name'] = trainer_name
	return render(request, 'trainer.html', {'profile_pic' : profile_pic, 'trainer_name' : trainer_name})

def form_signin(request):
	email = request.POST.get('email')
	md5_senha = hashlib.md5(request.POST.get('senha').encode('utf-8')).hexdigest()
	trainer = classes.acesso_banco()
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
	trainer = classes.acesso_banco()
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
