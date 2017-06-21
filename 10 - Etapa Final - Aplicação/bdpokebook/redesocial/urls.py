from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^index.html$', views.index, name='index'),
	url(r'^friends.html$', views.friends, name='friends'),
	url(r'^photos.html$', views.photos, name='photos'),
	url(r'^pokemon.html$', views.pokemon, name='pokemon'),
	url(r'^quest.html$', views.quest, name='quest'),
	url(r'^sign-up.html$', views.sign_up, name='sign-up'),
	url(r'^trainer.html$', views.trainer, name='trainer'),
	url(r'^submit$', views.submit, name='submit'),
]