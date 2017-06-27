from django.shortcuts import render
from django.http import HttpResponseRedirect
import pyodbc
import hashlib
from . import views

def index(request):
	return render(request, 'index.html')
	
def form_signin(request):
	email = request.POST.get('email')
	md5_senha = hashlib.md5(request.POST.get('senha').encode('utf-8')).hexdigest()
	trainer = views.acesso_banco()
	if trainer.login(email, md5_senha):
		request.session['trainer_id'] = email
		return render(request, 'trainer.html')
	else:
		return render(request, 'index.html', {'erro' : "O e-mail ou a senha estão errados"})