import xml.etree.ElementTree as ET
import csv
import os

ETree = ET.parse("marvel_simplificado.xml")

path='dadosMarvel'
if not os.path.exists(path):
    os.makedirs(path)
os.chdir(path)

universe = ETree.getroot()

heroes_all = open("heroes.csv", "w", newline='')
heroes_good = open("heroes_good.csv", "w", newline='')
heroes_bad = open("heroes_bad.csv", "w", newline='')
writer_all = csv.writer(heroes_all,delimiter=",",quoting=csv.QUOTE_MINIMAL)
writer_good = csv.writer(heroes_good,delimiter=",",quoting=csv.QUOTE_MINIMAL)
writer_bad = csv.writer(heroes_bad,delimiter=",",quoting=csv.QUOTE_MINIMAL)

good_num=0
bad_num=0
hero_num=0
hero_totalmass=0.0

for hero in universe:
    hero_num+=1
    hero_totalmass+=float(hero.find('weight_kg').text)
    if hero.find('name').text=="Hulk":
        hulk_bmi=float(hero.find('weight_kg').text)/(float(hero.find('height_m').text)**2)
    row_list = [hero.get('id')]
    
    for tag in hero:
        row_list.append(tag.text)
    writer_all.writerow(row_list)
    
    if hero.find('alignment').text=="Good":
        writer_good.writerow(row_list)
        good_num+=1
    elif hero.find('alignment').text=="Bad":
        writer_bad.writerow(row_list)
        bad_num+=1
        
print("A razão entre heróis bons/maus é %s/%s" % (good_num,bad_num))
print("O peso médio dos heróis é %s" % str(hero_totalmass/hero_num))
print("O IMC do Hulk é %s" % hulk_bmi)
    
heroes_all.close()
heroes_good.close()
heroes_bad.close()
