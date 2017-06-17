from django.shortcuts import render

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
	return render(request, 'trainer.html')	

# Create your views here.
