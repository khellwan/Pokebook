#!/usr/bin/python

import os
import xml.dom.minidom

newpath = r'dadosMarvel' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

DOMTree = xml.dom.minidom.parse("marvel_simplificado.xml")

os.chdir("dadosMarvel")

file_1 = open("herois.csv","w")
file_2 = open("herois_good.csv", "w")
file_3 = open("herois_bad.csv", "w")

bons = 0
maus = 0
total_herois = 0
soma_peso = 0.0


universe = DOMTree.documentElement

heroes = universe.getElementsByTagName("hero")

#Creating CSV File for all heroes
for hero in heroes:
    name = hero.getElementsByTagName('name')[0]
    popularity = hero.getElementsByTagName('popularity')[0]
    alignment = hero.getElementsByTagName('alignment')[0]
    gender = hero.getElementsByTagName('gender')[0]
    height_m = hero.getElementsByTagName('height_m')[0]
    weight_kg = hero.getElementsByTagName('weight_kg')[0]
    hometown = hero.getElementsByTagName('hometown')[0]
    intelligence = hero.getElementsByTagName('intelligence')[0]
    strength = hero.getElementsByTagName('strength')[0]
    speed = hero.getElementsByTagName('speed')[0]
    durability = hero.getElementsByTagName('durability')[0]
    energy_Projection = hero.getElementsByTagName('energy_Projection')[0]
    fighting_Skills = hero.getElementsByTagName('fighting_Skills')[0]  
    
    file_1.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (hero.getAttribute("id"), name.childNodes[0].data, popularity.childNodes[0].data, alignment.childNodes[0].data, gender.childNodes[0].data, height_m.childNodes[0].data, weight_kg.childNodes[0].data, hometown.childNodes[0].data, intelligence.childNodes[0].data, strength.childNodes[0].data, speed.childNodes[0].data, durability.childNodes[0].data, energy_Projection.childNodes[0].data, fighting_Skills.childNodes[0].data))
    total_herois += 1
    soma_peso += int(weight_kg.childNodes[0].data)

    if name.childNodes[0].data == "Hulk":
	imc_hulk = float(weight_kg.childNodes[0].data) / float(height_m.childNodes[0].data) / float(height_m.childNodes[0].data)

    if alignment.childNodes[0].data == "Good":
	bons += 1
        file_2.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (hero.getAttribute("id"), name.childNodes[0].data, popularity.childNodes[0].data, alignment.childNodes[0].data, gender.childNodes[0].data, height_m.childNodes[0].data, weight_kg.childNodes[0].data, hometown.childNodes[0].data, intelligence.childNodes[0].data, strength.childNodes[0].data, speed.childNodes[0].data, durability.childNodes[0].data, energy_Projection.childNodes[0].data, fighting_Skills.childNodes[0].data))
    
    if alignment.childNodes[0].data == "Bad":
	maus += 1
        file_3.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (hero.getAttribute("id"), name.childNodes[0].data, popularity.childNodes[0].data, alignment.childNodes[0].data, gender.childNodes[0].data, height_m.childNodes[0].data, weight_kg.childNodes[0].data, hometown.childNodes[0].data, intelligence.childNodes[0].data, strength.childNodes[0].data, speed.childNodes[0].data, durability.childNodes[0].data, energy_Projection.childNodes[0].data, fighting_Skills.childNodes[0].data))

file_1.close()
file_2.close()
file_3.close()

media_peso = soma_peso / total_herois

print "A proporcao de herois bons/mals eh de %s/%s" % (bons, maus)

print "A media dos pesos dos herois eh de %s" % media_peso

print "O IMC do Hulk eh igual a %s" % imc_hulk

	
