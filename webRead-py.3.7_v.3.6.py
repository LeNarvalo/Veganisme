# -*- coding: utf8 -*-
import webbrowser
from socket import gethostbyname, gethostname
from urllib.request import urlopen, urlretrieve
import unidecode
import threading
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import os, shutil, glob, sys
import time
import winsound
from pyunpack import Archive
import winshell
from win32com.client import Dispatch
from functools import partial
from pathlib import Path
 
master=Tk()
master.withdraw()
master.configure(background='#535353')
master.title("Véganisme - Rechercher / Koreus.com (v.3.6)")

###########
#VARIABLES#
###########
global derTxt, texto, o, bar
class testON:
	impossible=False
nbOfPages = 229
derTxt = ""
value = ""
displayVideo = False
displayImage = False
idAfter = []
listResult = []
listCom = []
dico = {}
dicoVid = {}
dicoImg = {}
chemin = os.path.expanduser('~\Veganisme')
balises=["<br />"]#"<blockquote>"#'<div class="xoopsQuote">'
accents=[["\xc3\xa7","ç"],["\xc3\x87","ç"],["\xe2\x80\x99","'"],["\xc3\xa9","é"],["\xc3\xa0","à"],["\xc3\xa8","è"],["\xc3\xb4","ô"],["\xc3\xb9","ù"],["\xc3\xaa","ê"],\
		["\xc3\xae","î"],["\xc3\xaf","ï"],["\xc3\xbb","û"],["\xc3\xa2","â"],["\xc5\x93","œ"],["\xc2\xa0",""],["\xc3\x89","É"],["\xe2\x80\x94","—"],["\xc3\x80","À"],\
		["\xc2\xab","«"],["\xc2\xbb","»"],["\xe2\x82\xac","€"]]
accents2=[["\\xc3\\xa7","\xc3\xa7"],["\\xc3\\xae","\xc3\xae"],["\\xc3\\x87","\xc3\x87"],["\\xe2\\x80\\x99","\xe2\x80\x99"],["\\xc3\\xa9","\xc3\xa9"],["\\xc3\\xa0","\xc3\xa0"],\
		["\\xc3\\xa8","\xc3\xa8"],["\\xc3\\xb4","\xc3\xb4"],["\\xc3\\xb9","\xc3\xb9"],["\\xc3\\xaa","\xc3\xaa"],["\\xc3\\xaf","\xc3\xaf"],["\\xc3\\xbb","\xc3\xbb"],\
		["\\xc3\\xa2","\xc3\xa2"],["\\xc5\\x93","\xc5\x93"],["\\xc2\\xa0","\xc2\xa0"],["\\xc3\\x89","\xc3\x89"],["\\xe2\\x80\\x94","\xe2\x80\x94"],["\\xc3\\x80","\xc3\x80"],\
		["\\xc2\xab","\\xc2\\xab"],["\\xc2\\xbb","\xc2\xbb"],["\\xe2\\x82\\xac","\xe2\x82\xac"]]
d = ['''<!DOCTYPE html>
<style>
table {
	width:100%;
}
table, th, td {
	border: 1px solid black;
	border-collapse: collapse;
}
th, td {
	padding: 15px;
	text-align: left;
}
table#t01 tr:nth-child(even) {
	background-color: #eee;
}
table#t01 tr:nth-child(odd) {
background-color: #fff;
}

</style>
<body>
<table id="t01">
''']
if not os.path.exists(chemin):  
	os.mkdir(chemin)
try:
	master.iconbitmap(chemin+'\\vegico.ico')
except:
	None

online = True #Pour tests de developpement
try:
	file = open(chemin+"\\Params.txt","r")
	strParams = file.read()
	file.close()
	online = int(strParams)
except:
	file = open(chemin+"\\Params.txt","w")
	file.write("1")
	file.close()
#####################
#GET NUMBER OF PAGES#
#####################
if online:
	try:
		pageTest=urlopen('https://www.koreus.com/modules/newbb/topic160787.html') 
		strpageTest=pageTest.read().decode('utf-8')
		splitText = '''<b>(1)</b> <a href="/modules/newbb/topic160787-20.html">2</a> <a href="/modules/newbb/topic160787-40.html">3</a> <a href="/modules/newbb/topic160787-60.html">4</a> ... <a '''
		listSST = strpageTest.split(splitText)
		listEST = listSST[1].split("</a>")
		listNSST = listEST[0].split(">")
		nbOfPages = int(listNSST[1])
	except:
		messagebox.showinfo("Connexion internet", '''La connexion au site est impossible, le logiciel va se lancer en mode OFFLINE.\n\
Vous pouvez revenir en mode ONLINE en cliquant sur la coche @.\n''')
		online=False

#####################
#   GET RACCOURCIS  #
#####################
try:
	file = open(chemin+"\\Raccs.txt","r")
	strRacc = file.read()
	file.close()
	nelleKey = int(strRacc[strRacc.index('NlleRacc :')+len('NlleRacc :'):strRacc.index('#')])
	escapeKey = int(strRacc[strRacc.index('EscRacc :')+len('EscRacc :'):strRacc.index('¤')])
except:
	file = open(chemin+"\\Raccs.txt","w")
	file.write("EscRacc :27¤"+"\n")
	file.write("NlleRacc :46#"+"\n")
	nelleKey=27
	escapeKey=46
	file.close()
	print('Bug Raccourcis')

######################
# DELETE OLD VERSION #
######################	
if online:
	try:
		urlHost = 'http://hostmajveganisme1.e-monsite.com/'
		page=urlopen(urlHost)
		strpage=page.read().decode('utf-8')
		lastMAJ=strpage[strpage.index('<li><strong>Nom du fichier : </strong>')+len('<li><strong>Nom du fichier : </strong>'):strpage.index('</li>')]
		sizeMAJ=int(float(strpage[strpage.index('<strong>Taille : </strong>')+len('<strong>Taille : </strong>'):strpage.index(' Mo')])*1000000)
		linkMAJ=strpage[strpage.index('<a href="')+len('<a href="'):strpage.index('" title="')]
		fullPath = chemin+"\\"+lastMAJ
		#print(lastMAJ)
		#print(linkMAJ)
		#print(fullPath)
		#print(sizeMAJ)
	except:
		fullPath = "INACESSIBLE"
		print('Bug MAJ')

def createShortCut():
	desktop = winshell.desktop()	
	path = os.path.join(desktop, "Veganisme.lnk")
	target = fullPath+"\\"+lastMAJ+".exe"
	wDir = fullPath
	icon = fullPath+"\\"+lastMAJ+".exe"
	shell = Dispatch('WScript.Shell')
	shortcut = shell.CreateShortCut(path)
	shortcut.Targetpath = target
	shortcut.WorkingDirectory = wDir
	shortcut.IconLocation = icon
	shortcut.save()

def download():
	global o
	print("Téléchargement en cours")
	urlretrieve(linkMAJ, chemin+"\\"+lastMAJ+".zip")
	print("Extract en cours")
	Archive(chemin+"\\"+lastMAJ+".zip").extractall(chemin)
	os.remove(chemin+"\\"+lastMAJ+".zip")
	print("Trying to launch new version")
	os.startfile(fullPath+"\\"+lastMAJ+".exe")
	try:
		createShortCut()
	except:
		print("Bug à la MAJ des raccourcis")
	oExit()

def getSizeOfDown():
	try:
		bar['value']=int(Path(chemin+"\\"+lastMAJ+".zip").stat().st_size)
	except:
		print("Bug Download Bar : Le chemin n'existe probablement pas encore !")

	while bar.cget('value')<sizeMAJ:
		time.sleep(0.5)
		getSizeOfDown()

def oExit():
	global o
	o.destroy()

if online:
	if fullPath != "INACESSIBLE":
		if not os.path.exists(fullPath):
			print('Mise à jour disponible')
			down_thread = threading.Thread(target=download)
			down_thread.start()
			o = Toplevel()
			o.overrideredirect(True)
			o.configure(width=200)
			x = (o.winfo_screenwidth()*0.85 - o.winfo_reqwidth())/2
			y = o.winfo_reqheight()
			o.geometry("+%d+%d" % (x, y))
			lbl = Label(o, text="Mise à jour du logiciel")
			lbl.grid(row=0, column=0, sticky=W+E)
			bar = Progressbar(o, orient='horizontal', mode='determinate', value=0, maximum=sizeMAJ)
			bar.grid(row=1, column=0, sticky=W+E)
			threading.Thread(target=getSizeOfDown).start()
			OK = Button(o, overrelief=GROOVE, text ='OK', command=oExit)
			OK.grid(row=2)
			#bar.start(1)
			o.mainloop()

	listDir = os.listdir(chemin)
	for dir in listDir:
		if dir.startswith("webRead") and dir.lower()!=lastMAJ.lower():
			try:
				shutil.rmtree(chemin+'\\'+dir)
			except:
				None

def windowsAlert():
	windowsAnswer = messagebox.askyesno("Continuer?", "Le script va supprimer toutes les archives permettant la recherche, voulez vous continuer?")
	return windowsAnswer
	
def windowsHelp():
	messagebox.showinfo("Aide", '''Raccourcis :\n\
- Tabulation pour naviguer sans souris\n\
- Entrée pour lancer la recherche\n\
- * dans la zone Auteur pour sélectionner tous les auteurs\n\
- * dans la zone Texte pour sélectionner tous les  commentaires d'un auteur\n\
- Les " dans la zone Texte permettent de chercher un enchainement de mot. Ex : "véganisme bonne ou mauvaise chose"\n\
\n\
Boutons :\n\
- Casse : Prendre en compte les accents et majuscules\n\
- Image : Rechercher uniquement les images\n\
- Video : Rechercher uniquement les vidéos\n\
- Rechercher : Lancer la recherche\n\
- Supprimer l'archivage : Supprimer les archives Sujet, Videos et Images. \n\
- Nouvelle recherche : Supprimer les paramètres de recherche saisis.\n\
- @ : Activer/Désactiver la connexion à internet''')
	
def createFPList(strpage):
	#LISTE N° FORUMPOST
	global listCom #Liste de forumpost en string
	a = strpage.split('''<a id="f''')			
	for l in a:
		if l.startswith('orumpost'):
			comNb= l.split('">')[0]
			listCom.append(comNb[8:])
			
def getDicoFromStr(file,type='str'):
	#OBTIENT DICO DEPUIS FICHIER SUJET.HTML EN STR UTF8
	global dico, dicoVid, dicoImg
	
	list = file.split("[#aut:")
	for line in list[1:]:		
		if "#aut]" in line:
			auteur = line[:line.index("#aut]")]
			if type == 'str':
				dico[auteur]=[]
			elif type == 'img':
				dicoImg[auteur]=[]
			elif type == 'vid':
				dicoVid[auteur]=[]
		comstr = line[line.index("[#coms:\n")+8:line.index("#coms]\n\n\n")]
		coms = comstr.split("#---------------------------------------------------------------------\n")
		for com in coms[:-1]:
			page = com[com.index('#Page:')+6:com.index('\n#ForumPost:')]
			if type == 'str':
				fp = com[com.index('#ForumPost:')+11:com.index('\n#Text:')]
				comm = com[com.index('#Text:')+6:-1]
				dico[auteur].append([page,fp,comm])
			elif type == 'img':
				fp = com[com.index('#ForumPost:')+11:com.index('\n#Image:')]
				img = com[com.index('#Image:')+7:-1]
				dicoImg[auteur].append([page,fp,img])
			elif type == 'vid':
				fp = com[com.index('#ForumPost:')+11:com.index('\n#Video:')]
				vid = com[com.index('#Video:')+7:-1]
				dicoVid[auteur].append([page,fp,vid])
	#print(dico.keys())

	if type == 'str':
		return dico
	elif type == 'img':
		return dicoImg
	elif type == 'vid':
		return dicoVid		
	
def dicoAndWriteStr(startrange=1980):
	#OBTIENT LES DICTIONNAIRES ET ECRIT LES FICHIERS SUJET.TXT IMAGES.TXT VIDEOS.TXT
	global listCom, dico, dicoVid, dicoImg, texto, derTxt, research_thread
	page=urlopen('https://www.koreus.com/modules/newbb/topic160787.html')
	strpage=page.read().decode('utf-8')
	suf = range(startrange,9999, 20)		
	countPage = 0
	countComm = -1
	pCurrent.stop()
	pCurrent['mode'] = "determinate"

	while suf[countPage]!=lastPage:			
		lastLenPage=len(strpage)
		createFPList(strpage)
		#DICO DES COMM/AUTEUR		
		b = strpage.split('href="/memb')
		for c in b:
			if c.startswith('re/'):
				countComm += 1
				e = c.split('">')
				i = e[1].split('</a>')
				auteur = i[0]
				f = c.split('<div class="comText')
				f1 = f[1]
				h = f1.split('</div>\r\n\t    <br clear="all" />') #h[0] = ComText uniquement
				h02 = h[0][2:]
				##REMOVE IMG
				imgs = []
				while "<img" in h02:
					idS = h02.index("<img")
					idE = h02[idS:].index(">")
					img = h02[idS:idS+idE+1]
					h02=h02.replace(img,"")
					imgs.append(img)

				##REMOVE VID
				vids = []
				while "<iframe" in h02 :
					idS = h02.index("<iframe")
					idE = h02[idS+10:].index(">") 
					vid = h02[idS:idS+idE+11]
					h02=h02.replace(vid,"")
					vids.append(vid)
				
				if auteur in dico:
					if listCom[countComm] not in dico[auteur]:
						dico[auteur].append([str(suf[countPage]),listCom[countComm],h02])
				else:
					dico[auteur]=[[str(suf[countPage]),listCom[countComm],h02]]
				
				count = 0
				for img in imgs:	
					if auteur in dicoImg:
						if listCom[countComm]+'-'+str(count) not in dicoImg[auteur]:
							dicoImg[auteur].append([str(suf[countPage]),listCom[countComm]+'-'+str(count),img])
					else:
						dicoImg[auteur]=[[str(suf[countPage]),listCom[countComm]+'-'+str(count),img]]
					count+=1

				count=0
				for vid in vids:
					if auteur in dicoVid:
						if listCom[countComm]+'-'+str(count) not in dicoVid[auteur]:
							dicoVid[auteur].append([str(suf[countPage]),listCom[countComm]+'-'+str(count),vid])
					else:
						dicoVid[auteur]=[[str(suf[countPage]),listCom[countComm]+'-'+str(count),vid]]
					count+=1
						
		countPage+=1		
		page=urlopen('https://www.koreus.com/modules/newbb/topic160787-'+str(suf[countPage])+'.html')
		strpage=page.read().decode('utf-8')
		pCurrent['value'] = countPage
		
	#ARCHIVAGE
	derTxt = "\n"+"ECRITURE EN COURS"
	texto.insert(END, derTxt)
	dics = [dico,dicoImg,dicoVid]
	for dic in dics:
		if dics.index(dic) == 0:
			file = open(chemin+"\\Sujet.txt","w",encoding="utf8")
			file.write('DICOSTR-DATE DU DERNIER ARCHIVAGE :'+str(time.localtime()[3])+'h'+str(time.localtime()[4])+'m - '+str(time.localtime()[2])+'/'+str(time.localtime()[1])+'/'+str(time.localtime()[0])+'\n')
		elif dics.index(dic) == 1:
			file = open(chemin+"\\Images.txt","w",encoding="utf8")
			file.write('DICOIMG-DATE DU DERNIER ARCHIVAGE :'+str(time.localtime()[3])+'h'+str(time.localtime()[4])+'m - '+str(time.localtime()[2])+'/'+str(time.localtime()[1])+'/'+str(time.localtime()[0])+'\n')
		elif dics.index(dic) == 2:
			file = open(chemin+"\\Videos.txt","w",encoding="utf8")
			file.write('DICOVID-DATE DU DERNIER ARCHIVAGE :'+str(time.localtime()[3])+'h'+str(time.localtime()[4])+'m - '+str(time.localtime()[2])+'/'+str(time.localtime()[1])+'/'+str(time.localtime()[0])+'\n')
		biggestPage = '0'
		for auteur in dic.keys():
			file.write('[#aut:'+auteur+"#aut]\n\n")
			file.write("[#coms:\n")
			for obj in dic[auteur]:					
					file.write("#Page:"+obj[0]+"\n") #BUG ICI
					if int(obj[0])>int(biggestPage):
						biggestPage=obj[0]
					file.write("#ForumPost:"+obj[1]+"\n")
					if dics.index(dic) == 0:
						file.write("#Text:"+obj[2]+"\n")
					elif dics.index(dic) == 1:
						file.write("#Image:"+obj[2]+"\n")					
					elif dics.index(dic) == 2:
						file.write("#Video:"+obj[2]+"\n")
					file.write("#---------------------------------------------------------------------\n")					 
			file.write("#coms]\n\n\n")
		file.write("\n"+str(lastLenPage)+"-"+biggestPage)
		file.close()
	
def rechercher():
	global listCom, dico, texto, derTxt, research_thread, lastPage, dicoImg, dicoVid
	#SUPPRIMER LES PRECEDENTES RECHERCHES
	files = glob.glob(chemin+'/*')
	for f in files:
		if f.endswith('.html'):
			os.remove(f)

	#ENREGISTRE LE SUJET/MET A JOUR L'ARCHIVAGE/RECHERCHE L'EXTRAIT DU TEXTE EN FONCTION DE L'AUTEUR

	if online:
		lastPage=int(nbOfPages)*20 #LAST PAGE + (1*20)
	
	#PREMIERE UTILISATION (CREATION DES ARCHIVES SUR LE DISQUE DUR)
	filesName = ["Sujet.txt","Images.txt","Videos.txt"]
	premiere_utilisation=False
	for fname in filesName:
		if not os.path.isfile(chemin+'\\'+fname):
			if not os.path.exists(chemin):  
				os.mkdir(chemin)
			file = open(chemin+"\\"+fname,"w")
			file.close()
			derTxt = "\n"+"CETTE OPERATION PEUT PRENDRE UN PEU DE TEMPS!"+"\n"+"ELLE N'A LIEU QU'A LA PREMIERE UTILISATION DU LOGICIEL OU APRES SUPPRESSION DE L'ARCHIVAGE."
			texto.insert(END, derTxt)
			listCom = []		
			dicoAndWriteStr(startrange=0)
			premiere_utilisation=True
			break #dicoAnWriteStr écrit les 3 dictionnaires et les fichiers correspondants
		
	#ARCHIVAGE DEJA EXISTANT
	if not premiere_utilisation:
		derTxt = "\n"+"RECUPERATION DE LA BASE"
		texto.insert(END, derTxt)
		if len(dico) < 1:
			file = open(chemin+"\\Sujet.txt","r",encoding="utf8")
			fileStr = file.read()
			file.close()
			dico = getDicoFromStr(fileStr,'str')
		if len(dicoImg) < 1:
			file = open(chemin+"\\Images.txt","r",encoding="utf8")
			fileImg = file.read()
			file.close()
			dicoImg = getDicoFromStr(fileImg,'img')
		if len(dicoVid) < 1:
			file = open(chemin+"\\Videos.txt","r",encoding="utf8")
			fileVid = file.read()
			file.close()
			dicoVid = getDicoFromStr(fileVid,'vid')
	
		#VERIFICATION DE LA MISE A JOUR
		if online:
			derTxt = "\n"+"VERIFICATION DE LA MISE A JOUR DE LA BASE"
			texto.insert(END, derTxt)
			file = open(chemin+"\\Sujet.txt","r",encoding="utf8")
			fileList = file.readlines()
			file.close()
			lastLenPage = int(fileList[-1][:fileList[-1].index('-')])
			lastPageInMemory =int(fileList[-1][fileList[-1].index('-')+1:])
			listCom = []
			suf = range(lastPageInMemory,9999, 20)		
			countPage = 0		
			page=urlopen('https://www.koreus.com/modules/newbb/topic160787-'+str(suf[countPage])+'.html')
			strpage=page.read().decode('utf-8')
			news = True
			while suf[countPage]!=lastPage:
				if len(strpage) == lastLenPage:
					news = False
				if len(strpage) != lastLenPage:				
					news = True
				countPage+=1
				page=urlopen('https://www.koreus.com/modules/newbb/topic160787-'+str(suf[countPage])+'.html')
				strpage=page.read().decode('utf-8')
			
			if not news:
				derTxt = "\n"+"BASE A JOUR!"
				texto.insert(END, derTxt)
		
			if news:
				derTxt = "\n"+"MISE A JOUR DE LA BASE..."
				texto.insert(END, derTxt)
				dicoAndWriteStr(startrange=lastPageInMemory-20) #-20 indispensable cf. la fonction en question
						
	
	research_thread = threading.Thread(target=research)
	research_thread.daemon = True
	research_thread.start()

def research():
	global listResult, texto, derTxt, result, entree2, auteurs, videos_found, imgs_found
	#RECHERCHER PAR AUTEUR L'EXTRAIT
	try:
		derTxt = "\n"+"RECHERCHE EN COURS..."
		texto.insert(END, derTxt)
		pCurrent['mode'] = "indeterminate"
		pCurrent.start(1)
		result = 0
		if image.get():
			dic = dicoImg
			imgs_found = []
		elif video.get():
			dic = dicoVid
			videos_found = []
		else:
			dic = dico
			listResult = []

		keys = []
		for key in dic.keys():
			keys.append(key)
		#print(keys)

		for auteur in auteurs:			
			if auteur not in keys:
				derTxt = "\n"+auteur+" AUTEUR NON TROUVE"
				texto.insert(END, derTxt)
				continue

			if dic == dicoVid:
				videos_found.append([auteur,int(len(dic[auteur])),dic[auteur]])

			elif dic == dicoImg:
				imgs_found.append([auteur,int(len(dic[auteur])),dic[auteur]])

			elif dic == dico:
				for comm in dic[auteur]:
					page = comm[0]
					fp = comm[1]
					txt = comm[2]
					try:						
						comm1 = txt
						for a in accents:
							comm1 = comm1.replace(a[0],a[1])
						if not casse.get():
							try:
								comm2 = unidecode.unidecode(comm1.lower())
							except:
								print("BUG ENCODAGE : "+comm1)
								#comm2 = comm1.lower() #Inutile normalement
						
						else:
							comm2 = comm1
						
						if entree2 == "*":
							listResult.append([page,fp,comm2,auteur,0])
							result+=1
						else:
							if entree2.count('"') != 2:
								listEntree = entree2.split(' ')
								while ' ' in listEntree:
									listEntree.remove(' ')
							else:
								listEntree = [entree2.replace('"',''),]
															
							motPresent = False
							listIdSpan = []
							listMotInComm = []
							for mot in listEntree:							
								if mot in comm2 and len(comm2.split())>1:								
									listMotInComm.append(comm2.index(mot))								
									motPresent = True
									countMot = comm2.count(mot)
									if casse.get():
										idOpenSpan = comm2.index(mot)
										idCloseSpan = idOpenSpan+len(mot)
										listIdSpan.append([idOpenSpan,idCloseSpan])
									else:
										idOpenSpan = comm2.index(mot)
										idCloseSpan = idOpenSpan+len(mot)
										listIdSpan.append([idOpenSpan,idCloseSpan])
		
							if motPresent:
								for list in listIdSpan[::-1]:
									comm2 = comm2[:list[1]]+"</span>"+comm2[list[1]:]
									comm2 = comm2[:list[0]]+'<span style="background-color: #DA81F5;" >'+comm2[list[0]:]						
			
								b = []
								for a in listMotInComm:
									b.append(a)
								b.sort()
			
								d = [] #liste classement
								for c in listMotInComm:
									d.append(b.index(c))
			
								points = len(listMotInComm)+countMot/2 #Points de pertinence
								lastId = -1
								for id in d:
									if id-1 == lastId:
										points += 3
									elif id+1 == lastId:
										points += 2
									else:
										points += 1
									lastId = id
			
								idInsert = -1
								for l in listResult:
									if points > l[4]: #Trier par pertinence
										idInsert = listResult.index(l)	
										break
									if l[4] == points:
										if l[0] > page: #Trier par page
											idInsert = listResult.index(l)
											break
										idInsert = listResult.index(l)+1
								if idInsert>-1:
									listResult.insert(idInsert,[page,fp,comm2,auteur,points])
								else:
									listResult.append([page,fp,comm2,auteur,points])
	
								#if result < 200:
								#	derTxt = "\n"+"PAGE:"+str((int(page)+20)/20)+"    FORUMPOST :"+str(num)
								#	texto.insert(END, derTxt)
								result += 1	
							
					except:
						None

				
		buildPageWeb_thread = threading.Thread(target=buildPageWeb)
		buildPageWeb_thread.daemon = True
		buildPageWeb_thread.start()
		#derTxt = "\n"+"AUTEUR NON TROUVE"
		#texto.insert(END, derTxt)
		#pCurrent.stop()
	except:
		None

def clignotement():
	global clignotant, Afficher, idAfter
	if not clignotant:
		Afficher['fg']="black"
		clignotant=True
		idAfter.append(master.after(250,clignotement))
	else:
		Afficher['fg']="#088A08"
		clignotant = False
		idAfter.append(master.after(250,clignotement))

def buildPageWeb():
	global texto, derTxt, entree2, clignotant, idAfter
	pCurrent.stop()
	clignotant =True
	if not image.get() and not video.get():
		if SoundVar.get() and result>0:
			winsound.Beep(1500,50)
			winsound.Beep(2500,50)
			winsound.Beep(3500,50)
			winsound.Beep(4500,50)
		if SoundVar.get() and result==0:
			winsound.Beep(1500,50)
			winsound.Beep(1000,50)
			winsound.Beep(500,50)
			winsound.Beep(250,50)
		if result >= 200:
			derTxt=""
			texto.delete(1.0, END)
			derTxt = "\n"+"Nombre de resultats : >200"
			texto.insert(END, derTxt)
			Afficher['state']='normal'
			Afficher['text']='Afficher > 200 résultats'
			Afficher['fg']="red"
			if entree2 != "*":
				return
			
		if result < 200:	
			derTxt = "\n"+"Nombre de resultats : "+str(result)
			texto.insert(END, derTxt)
			Afficher['state']='normal'
			Afficher['text']='Afficher '+str(result)+' résultat(s)'
			Afficher['fg']="#088A08"
			idAfter.append(master.after(250,clignotement))

		for id in idAfter:
			master.after_cancel(id)

		Afficher['fg']="#088A08"
		e = '''<meta charset="CP1252">
		<!DOCTYPE html>
		<html>
		<head>		
		<style>
		table {
			width:100%;
		}
		table, th, td {
			border: 1px solid black;
			border-collapse: collapse;
		}
		th, td {
			padding: 15px;
			text-align: left;
		}
		table#t01 tr:nth-child(even) {
			background-color: #e0dfe7;
		}
		table#t01 tr:nth-child(odd) {
		background-color: #fff;
		}
		
		blockquote {
			border-left: 3px solid #ccc;
		}
		
		img.bas {
			float: left;
			vertical-align: text-bottom;
		}
		
		</style>
		</head><table id="t01" cellpadding="3px" cellspacing="0px" rules="all" style="border:solid 1px black; border-collapse:collapse; text-align:center;">
		'''
		if casse.get():
			entree2 = entree2
		try:
			aut = unidecode.unidecode(entreeAuteur.get())
		except:
			aut = entreeAuteur.get()
		aut = aut.replace(";"," ")
		if len(aut.split())>5:
			aut = aut[:50]+"[...]"
		pageWeb = open(chemin+"\\pageWeb.html","w",encoding="cp1252")
		pageWeb.write(e)
		pageWeb.write('''<tr><th colspan="2" style="height:80px ; background-color: #bebcc9 ; padding: 0px ">
		<p style="text-align: right ; font-size: 14px ; font-weight: normal ; font-family: Helvetica ; color: #fff" >
		<a href="https://www.koreus.com/"><img class="bas" align="left" src="https://koreus.cdn.li/static/images/logo.jpg"></a>
		<a href="http://hostmajveganisme1.e-monsite.com/"><img class="right" src="http://hostmajveganisme1.e-monsite.com/medias/images/vegico-2.png"></a>
		<br style="margin: 0px 0">
		Contact : <a style="color: #f9f9f9" href="https://www.koreus.com/modules/mpmanager/pmlite.php?send2=1&to_userid=160372">AymericCaron</a>
		</p>		
		</th>
		</tr>
		<tr>
		<th colspan="2" style="background-color:#9a9ace"><FONT color="#fff">'''+aut+''' - Extrait du texte recherché : '''+entree2+''' - <U>Nombre de résultat(s)</U> : '''+str(result)+'''</FONT></th>
		''')
	
		for list in listResult:
			txt = list[2]			
			for b in balises:
				txt = txt.replace(b,"\n")
			for a in accents:
				txt = txt.replace(a[0],a[1])
			try:
				start = txt.index('<span style="background-color: #DA81F5;" >')
				newStart = -1
				count = 250
				while newStart < 0:
					newStart = start - count
					count-=1
				txt = txt[newStart:]
			except:
				None
					
			try:
				id1=txt[:800][::-1].index('a<')
			except:
				id1=9999
			try:
				id2=txt[:800][::-1].index('>a/')
			except:
				id2=9999
				
			if id2 > id1:		
				txt2 = txt[:800-id1-1]
			else:
				txt2 = txt[:800]
			
			
			if len(txt)>800:
				txt2 += '[...]</div>'
				
			pageWeb.write('<tr><td>'+txt2.encode("cp1252","ignore").decode("cp1252")+'<div align="right"><font face="verdana" color="orange" size="2">-<i><b>'+str(list[3])+'</b></i></font></div><div align="right"><font face="verdana" color="#8A0808" size="1"><i><b>Pertinence : '+str(list[4])+'</b></i></font></div></td><td><a href="https://www.koreus.com/modules/newbb/topic160787-'+str(list[0])+'.html#forumpost'+str(list[1])+'"> Page '+str((int(list[0])+20)/20)+' / ForumPost.'+str(list[1])+'</a></td></tr>')

		pageWeb.close()
		displayPageWeb = threading.Thread(target=displaySearch,args=("str",))
		
	if video.get():
		nbOfVid = 0
		for vid in videos_found:
			derTxt = "\n"+vid[0]+" a partagé "+str(vid[1])+" vidéo(s)"
			texto.insert(END, derTxt)
			nbOfVid+=vid[1]

		if nbOfVid:
			Afficher['state']='normal'
			Afficher['text']='Afficher '+str(nbOfVid)+' vidéo(s)'
			Afficher['fg']="#088A08"
			idAfter.append(master.after(250,clignotement))
		e = '''<!DOCTYPE html>
		<meta charset="UTF-8">
		<html>
		<table>
		<style>
				table {
					width:100%;
				}
				thead,
				tfoot {
					background-color: #9a9ace;
					color: #fff;
				}
		</style>'''
		
		urls = ''
		for vids in videos_found:
			link = chemin+"\\pageWeb - "+vids[0]+".html"
			pageWeb = open(link,"w",encoding="utf8")
			pageWeb.write(e)
			urls += '<a href=".'+link[link.index("\\pageWeb"):]+'">'+vids[0]+'</a> / '
			pageWeb.close()


		
		for vids in videos_found:
			tdCount = 0
			pageWeb = open(chemin+"\\pageWeb - "+vids[0]+".html","a",encoding="utf8")
			pageWeb.write('<thead><tr><th colspan="3">'+urls+'</th></tr></thead>')
			pageWeb.write('<thead><tr><th colspan="3">'+vids[0]+' - '+str(vids[1])+' vidéo(s)</th></tr></thead>')
			for vid in vids[2]: #vids[2] = dic[auteur]=[[page,fp,vid]]
				#print(vid)
				url = vid[2][vid[2].index('data-src="')+len('data-src="'):vid[2].index('" frame')]
				fp = vid[1][:vid[1].index('-')]
				#print(url,vid[0],vid[1])
				tdCount += 1
				if tdCount == 1:
					pageWeb.write('<tr>\n')
				if len(vids[2]) < 3:
					width=33
				else:
					width=100
				pageWeb.write('<td><iframe src="'+url+'" width='+str(width)+'% height=100% frameborder="0"></iframe><br /><a href="https://www.koreus.com/modules/newbb/topic160787-'+str(vid[0])+'.html#forumpost'+str(fp)+'"> Page '+str((int(vid[0])+20)/20)+' / ForumPost.'+str(vid[1])+'</a></td>\n')
				#<iframe class=" lazyloaded" data-src="https://www.youtube.com/embed/4eA0SkIVGEU" allowfullscreen="" width="640" height="360" frameborder="0"></iframe></iframe>
				if tdCount % 3 == 0:
					pageWeb.write('</tr>\n')
			pageWeb.write('</table>')
			pageWeb.close()

	if image.get():
		#derTxt = "\n"+"Fonctionnalité non développée pour le moment"
		#texto.insert(END, derTxt)
		nbOfImg = 0
		for imgs in imgs_found:
			for img in imgs[2]:
				if "emoji" in img[2]:
					continue
				elif 'width="' in img[2]:
					width = int(img[2][img[2].index('width="')+len('width="'):img[2].index('" height=')])
					if width < 100:
						continue
					nbOfImg+=1
			derTxt = "\n"+imgs[0]+" a partagé "+str(nbOfImg)+" images(s)"
			texto.insert(END, derTxt)

		if nbOfImg:
			Afficher['state']='normal'
			Afficher['text']='Afficher '+str(nbOfImg)+' image(s)'
			Afficher['fg']="#088A08"
			idAfter.append(master.after(250,clignotement))
		e = '''<!DOCTYPE html>
		<meta charset="UTF-8">
		<html>
		<table>
		<style>
				table {
					width:100%;
				}
				thead,
				tfoot {
					background-color: #9a9ace;
					color: #fff;
				}
		</style>'''
		
		urls = ''
		for imgs in imgs_found:
			link = chemin+"\\pageWeb - "+imgs[0]+".html"
			pageWeb = open(link,"w",encoding="utf8")
			pageWeb.write(e)
			urls += '<a href=".'+link[link.index("\\pageWeb"):]+'">'+imgs[0]+'</a> / '
			pageWeb.close()

		for imgs in imgs_found:
			tdCount = 0
			pageWeb = open(chemin+"\\pageWeb - "+imgs[0]+".html","a",encoding="utf8")
			pageWeb.write('<thead><tr><th colspan="3">'+urls+'</th></tr></thead>')
			pageWeb.write('<thead><tr><th colspan="3">'+imgs[0]+' - '+str(nbOfImg)+' image(s)</th></tr></thead>')
			for img in imgs[2]:
				if "emoji" in img[2]:
					continue
				elif 'width="' in img[2]:
					width = int(img[2][img[2].index('width="')+len('width="'):img[2].index('" height=')])
					height = int(img[2][img[2].index('" height="')+len('" height="'):img[2].index('" src="')])
					if width < 100:
						continue
				url = img[2][img[2].index('data-src="')+len('data-src="'):img[2].index('" alt')]
				fp = img[1][:img[1].index('-')]
				ratio = width/300
				width = int(width/ratio)
				height = int(height/ratio)
				#print(url,img[0],img[1])
				tdCount += 1
				if tdCount == 1:
					pageWeb.write('<tr>\n')
				pageWeb.write('<td><img src="'+url+'" width='+str(width)+' height='+str(height)+'><br /><a href="https://www.koreus.com/modules/newbb/topic160787-'+str(img[0])+'.html#forumpost'+str(fp)+'"> Page '+str((int(img[0])+20)/20)+' / ForumPost.'+str(img[1])+'</a></td>\n')
				#<iframe class=" lazyloaded" data-src="https://www.youtube.com/embed/4eA0SkIVGEU" allowfullscreen="" width="640" height="360" frameborder="0"></iframe></iframe>
				if tdCount % 3 == 0:
					pageWeb.write('</tr>\n')
			pageWeb.write('</table>')
			pageWeb.close()

def displaySearch(argu):
	if not result:
		return
	if argu == "str":
		os.startfile("C:/Users/LeNa/Veganisme/pageWeb.html")

	elif argu == "vid":
		os.startfile("C:/Users/LeNa/Veganisme/pageWeb - "+str(videos_found[0][0])+".html")

	#Afficher['state']='disabled'
	
def testButtonImg():
	global ideo, bouton3
	if image.get():
		video.set(0)
		#image.set(0)
		texto.delete(1.0, END)
		#derTxt = "\n"+"Fonctionnalité non développée pour le moment"
		#texto.insert(END, derTxt)
		entreeText['state']='disabled'
	else:
		entreeText['state']='normal'

def testButtonVid():	
	global image, bouton2
	if video.get():
		image.set(0)
		texto.delete(1.0, END)
		entreeText['state']='disabled'
	else:
		entreeText['state']='normal'
	
def init2(evt=1):
	global search_thread, derTxt, texto, entree2, auteurs
	pCurrent['mode'] = "indeterminate"
	Afficher['state']='disabled'
	Afficher['text']='Afficher'
	texto.delete(1.0, END)
	derTxt=""
	for id in idAfter:
		master.after_cancel(id)
	
	try:
		os.remove(chemin+'\\pageWeb.html')
	except:
		None
	
	try:		
		c = 1
		while 1:
			os.remove(chemin+'\\pageWeb'+str(c)+'.html')
			c+=1
	except:
		None
	
	if len(entreeAuteur.get())==0:
		if SoundVar.get():
			winsound.Beep(500,50)
			winsound.Beep(300,50)
		derTxt = "VEUILLEZ SAISIR UN NOM D'AUTEUR ET UN EXTRAIT DU TEXTE QU'IL AURAIT SAISI"\
		+"\nTAPEZ * POUR SELECTIONNER TOUS LES AUTEURS"
		texto.insert(END, derTxt)
		return
	if len(entreeText.get())<5 and not image.get() and not video.get() and entreeText.get()!="*":
		if SoundVar.get():
			winsound.Beep(500,50)
			winsound.Beep(300,50)
		derTxt = "\n"+"L'EXTRAIT DE TEXTE EST TROP COURT (MIN 5 CARACTERES)"
		texto.insert(END, derTxt)
		return		
	auteur = entreeAuteur.get() #Unicode si accent, string sinon
	auteurs_list = auteur.split(";")
	while "" in auteurs_list:
		auteurs_list.remove("")
	auteurs = []
	for auteur in auteurs_list:
		auteurs.append(auteur)
		#try:
		#	auteurs.append(unidecode.unidecode(auteur))
		#except:
		#	auteurs.append(auteur)
		
	entree = entreeText.get() #Unicode si accent, string sinon
	if not casse.get():
		try:
			entree2 = unidecode.unidecode(entree.lower())
		except:
			entree2 = entree.lower()	
	else:
		entree2 = entree
	

	pCurrent.start(1)
	search_thread = threading.Thread(target=rechercher)
	search_thread.start()

def afficherRecherche():
	#buildPageWeb(True)
	files = glob.glob(chemin+'/*')
	for f in files:
		if f.endswith('.html'):
			os.startfile(f)
			return
	
def deleteSujet():
	if not windowsAlert():
		return
	try:
		try:
			os.remove(chemin+'\\Sujet.txt')
			derTxt = "\n"+"ARCHIVE SUJET SUPPRIMEE"
			texto.insert(END, derTxt)
		except:
			derTxt = "\n"+"ARCHIVE SUJET INEXISTANTE"
			texto.insert(END, derTxt)
		try:
			os.remove(chemin+'\\Images.txt')
			derTxt = "\n"+"ARCHIVE IMAGES SUPPRIMEE"
			texto.insert(END, derTxt)
		except:
			derTxt = "\n"+"ARCHIVE IMAGES INEXISTANTE"
			texto.insert(END, derTxt)	
		try:
			os.remove(chemin+'\\Videos.txt')
			derTxt = "\n"+"ARCHIVE VIDEOS SUPPRIMEE"
			texto.insert(END, derTxt)
		except:
			derTxt = "\n"+"ARCHIVE VIDEOS INEXISTANTE"
			texto.insert(END, derTxt)	
	except:
		derTxt = "\n"+"ARCHIVES INEXISTANTES"
		texto.insert(END, derTxt)

def OnRelease(event=1):
	global nameAuteur, value
	widget = event.widget
	selection=widget.curselection()
	values = []
	for sel in selection:
		values.append(widget.get(sel))	
	for val in values:
		if val == "AUTEUR INCONNU" or val=="REAFFICHER LA LISTE":
			createListAuteur()
			return
		if val in value:
			continue
		try:
			value += name.encode('utf8', 'ignore')
		except:
			value += val
		value += ";"	
	nameAuteur.set(value)
	createListAuteur()

def waitAfterSelectAut():
	entreeAuteur['state']= NORMAL
	
def createListAuteur(evt=1):	
	global listSel, taped, nameAuteur, value, lenEntree
	if not taped:
		master.after(50,createListAuteur)
		taped=True
		return
	if taped:
		taped=False		
	entree = entreeAuteur.get()	
	if not ";" in entree: #Permet de flusher value quand on supprime les auteurs sélectionés
		value=""
	else: #Permet de créer value si l'utilisateur n'utilise pas la liste mais tape directement auteur1;auteurs
		value=""
		for aut in entree.split(';')[:-1]:
			value+=aut+';'

	yDefilB = Scrollbar(master, orient='vertical')
	yDefilB.grid(row=0, column=3, sticky='nswe')
	listSel = Listbox(master, yscrollcommand=yDefilB.set, height=3, selectmode=EXTENDED)
	try:
		try:
			file = open(chemin+"\\Sujet.txt","r",encoding="UTF8")
			fileStr = file.read()
			file.close()
			dictio = getDicoFromStr(fileStr,'str')
			listNames = list(dictio.keys())
		except:
			listNames = ["Kanchi","-itz-","Biiiiiip","Lorihengrin","Olrik","Arsenick","kahlan","Invité","Pouip","Cornflake","Kasanoda","AshySlashy","Kirouille","Mazuru","Skara","leozero","Skity","maieuh","Loom-","Bend_ua","aioren","benboo","Turlutuutu","alvein","Norbert","Insert","Aethnight","Alex333","MusicMan","PPilou","carpet_bombing","A_Rod","-Stitch-","raphiol","Carraidas","Quokka","Surzurois","Chaoui","LeMat","alixoux","Clayton","papives","johnmacjohn","Swe_33","PIume","Mogliere","EdTheGrocer","Krobot","-ninja-","Guillotine","Wikiss","Zertyy","LaPelle","Asmodeus","-JoJo-","35445345","Archib","THE_ROYE","eck0es","jopopmk","Imnothere","Petis","Leviatan","Poum45","Zwitterion","TheLord","Simonello","Infame_ZOD","Plopp","Leeloochan","Avaruus","Rodhar","Marsu_Xp","WonderSarah","PandorZz","Miiiichel","izard","Admonitio","posteur","Rob2017","Skwatek","Weedol","Keussy","Ataync","_hans","Wiliwilliam","Vixen","Pam_en_Personne","icemelody","Fantomon","dylsexique","Madoss","-Flo-","Lachessis","Brocoli2","trachsel","Kingu","Tunkasina","RoseRose","edirol83","Zipane","sam54000","poiuytreza525","zafirbel","Jinroh","paulberger","Ragalok","Revenchard","titi46","Boboss","Staffie","madflo","wayne","arouen","fleurdumale","BartopGames","giny89","pigme","gazeleau","Takateck","quintus000","NPNLA","Scruffy","BigbroZ","fluffy","Bloodshed","Marjo12","digital3d","Poulpy","PurLio","foodstache","mariam21","Simone49","Milot","Faleba","AymericCaron","Vassili44","sebasgo","Ubbos","Yazguen","akrogames","Gigo12","Interfector"]
		listNames.sort(key=str.lower)
		listName = []
		if entree != "*":
			try:
				if ";" in entree:
					aut2 = entree.split(";")
					while " " in aut2:
						aut2.remove(" ")
					if not entree.endswith(";"):
						listEntree = entree.split(";")
						listName=[]						
						for name in listNames:
							if name.lower().startswith(listEntree[-1].lower()) and name not in aut2[:-1]:
								listName.append(name)
					else:
						if len(aut2)>=len(listNames):
							return
						for name in listNames:							
							if name not in aut2:
								listName.append(name)


				else:
					for name in listNames:
						if name.lower().startswith(entree.lower()):
							listName.append(name)	
			except:				
				None			
		else:
			listName = listNames
	except:
		listName = ["REAFFICHER LA LISTE"]		
		nameAuteur.set("")
	if not len(listName):
		listName = ["AUTEUR INCONNU"]
	for name in listName:
		listSel.insert(END,name)	
	if listSel.get(0)=="REAFFICHER LA LISTE":
		listSel.itemconfig(0, foreground="green")
	elif listSel.get(0)=="AUTEUR INCONNU":
		listSel.itemconfig(0, foreground="red")
	elif len(listName) == 1 and not entree.endswith(";") and len(entree)> lenEntree:
		if SoundVar.get():
			winsound.Beep(1000, 5)
			winsound.Beep(2500, 10)
		for name in listSel.get(0,END):
			try:
				value += name.encode('utf8', 'ignore')
			except:
				value += name
			value+=';'		
		nameAuteur.set(value)
		entreeAuteur.icursor(999)
		entreeAuteur['state']= 'readonly'
		master.after(1000,waitAfterSelectAut)
		createListAuteur()
		
	listSel.bind("<ButtonRelease-1>", OnRelease)
	listSel.grid(row=0, column=2, sticky='sew')
	if entree == u"*":
		listSel.select_set(0, END)
		value = ""
		for name in listSel.get(0,END):
			try:
				value += name.encode('utf8', 'ignore')
			except:
				value += name
			value += ";"
		nameAuteur.set(value)
		entreeAuteur.icursor(999) 
	yDefilB['command'] = listSel.yview

	lenEntree = len(entree)
	
def callback(event):
    # select text after 50ms
    master.after(50, select_all, event.widget)

def select_all(widget):
    # select text
    widget.select_range(0, 'end')
    # move cursor to the end
    widget.icursor('end')
	
def nelleRech():
	global Afficher, taped, nameAuteur, texto, pCurrent, textVar, casse, image, video
	Afficher['state']='disabled'
	Afficher['text']='Afficher'
	taped=False
	nameAuteur.set('')
	texto.delete(1.0, END)
	pCurrent.stop()
	pCurrent['mode'] = "determinate"
	pCurrent['value'] = 5
	textVar.set('')
	createListAuteur()
	casse.set(0)
	image.set(0)
	video.set(0)
	try:
		os.remove(chemin+'\\pageWeb.html')
	except:
		None
	
	try:		
		c = 1
		while 1:
			os.remove(chemin+'\\pageWeb'+str(c)+'.html')
			c+=1
	except:
		None
	entreeAuteur.focus_set()
		
def playTabSound(evt=1):
	if SoundVar.get():
		winsound.Beep(400,5)
		winsound.Beep(1000,10)
		
def testKey(evt):
	if evt.keycode == escapeKey:
		master.destroy()
		master.quit()
	elif evt.keycode == nelleKey:
		nelleRech()
	
def getNelleKey(evt):	
	global nelleKey, nleVar
	nelleKey = evt.keycode
	window.after(0,nleVar2,(nleVar))

def nleVar2(var):
	var.set('   [Code Touche : '+str(nelleKey)+']')
	
def getEscapeKey(evt):	
	global escVar,escapeKey
	escapeKey = evt.keycode
	window.after(0,escVar2,(escVar))
	
def escVar2(var):
	var.set('   [Code Touche : '+str(escapeKey)+']')
	
def blinkWindow(count=0):
	global window	
	if count % 2 == 0:
		color='#535353'
	else:
		color="white"
	if len(escVar.get())<5:
		entreeEsc['background']=color
	if len(nleVar.get())<5:
		entreeNle['background']=color
	if count<5:
		count+=1
		window.after(50,blinkWindow,(count))

def emptyRaccSound():
	winsound.PlaySound('SystemExit', winsound.SND_ALIAS)
	
def windowExit(event):
	global window
	if event:
		if len(escVar.get())<5 or len(nleVar.get())<5:
			sound_thread = threading.Thread(target=emptyRaccSound)
			sound_thread.daemon = True
			sound_thread.start()		
			blinkWindow()
		else:
			file = open(chemin+"\\Raccs.txt","w")
			file.write("EscRacc :"+str(escapeKey)+"¤\n")
			file.write("NlleRacc :"+str(nelleKey)+"#\n")
			window.destroy()
	else:
		window.destroy()
	
def determineRacc(count=0):
	global labelRac, window,entreeEsc,escVar,nleVar,entreeNle
	window = Toplevel()
	labelRac = Label(window, text="CONFIGURATION DES RACCOURCIS:")	
	labelRac.grid(row=0,column = 0, columnspan = 2)
	labelRac.focus_set()
	esc_label = Label(window, text="Quitter le programme :")
	esc_label.grid(row=1,column=0, sticky=W)
	escVar=StringVar()
	entreeEsc= Entry(window,textvariable=escVar)
	entreeEsc.bind('<Key>',getEscapeKey)
	entreeEsc.grid(row=1,column = 1, sticky=W)	
	nle_label = Label(window, text="Nouvelle recherche :")
	nle_label.grid(row=2,column=0, sticky=W)
	nleVar=StringVar()
	entreeNle= Entry(window, textvariable=nleVar)	
	entreeNle.bind('<Key>',getNelleKey)
	entreeNle.grid(row=2,column = 1, sticky=W)
	OK = Button(window, overrelief=GROOVE, text ='OK', command=partial(windowExit,1))
	OK.grid(row=3,column=0)
	ESC = Button(window, overrelief=GROOVE, text ='Quitter', command=partial(windowExit,0))
	ESC.grid(row=3,column=1)
	window.overrideredirect(True)
	window.mainloop()
	
def getAndSetParams():
	global online, testON
	try:
		if MAJVar.get():
			pageTest=urlopen('https://www.koreus.com/modules/newbb/topic160787.html')
			online=True
			try:
				if not testON.is_alive():
					testON = threading.Timer(2, testConnexion)
					testON.start()
					testON.impossible=False
					#print('testON is not alive')
			except:
				testON = threading.Timer(2, testConnexion)
				testON.start()
				#print('testON is started')
		else:
			online=False
			if testON.impossible==False:
				messagebox.showinfo("Connexion internet", '''La connexion au site a été coupée.\n''')
	except:
		online=False
		MAJVar.set(False)
		messagebox.showinfo("Connexion internet", '''La connexion au site est impossible.\n''')


def changeParams(event=1):
	master.after(50,getAndSetParams)
	

def testConnexion(timeout=1):
	global online, testON

	while True:
		if MAJVar.get():
			IP = gethostbyname(gethostname())
			#print(IP)
			testON.impossible=False
			if IP.startswith("127"):
				testON.impossible=True
				online=False
				MAJVar.set(False)
				messagebox.showinfo("Connexion internet", '''La connexion au site est impossible !\n''')
	
		time.sleep(0.05)

def fenetre():
	global Afficher, SoundVar, MAJVar, taped, nameAuteur, texto, pCurrent, entreeAuteur, entreeText, Rechercher, scrollbar, casse, image, video, bouton2, bouton3, textVar
	r = 0
	x = (master.winfo_screenwidth()*0.85 - master.winfo_reqwidth())/2
	y = (master.winfo_screenheight()*0.70 - master.winfo_reqheight())/2
	master.bind('<Return>', init2)
	master.bind('<Key>',testKey)
	master.geometry("+%d+%d" % (x, y))
	master.resizable(False, False)
		
	t1 = Frame(master).grid(row=r)
	auteur_label = Label(t1, text="Auteur :",bg='#535353',fg="white")
	auteur_label.grid(row=r,column=0, sticky=W)
	nameAuteur=StringVar()
	entreeAuteur = Entry(t1, textvariable=nameAuteur,width=1)
	taped=False
	createListAuteur()
	entreeAuteur.bind('<Control-a>', callback)
	entreeAuteur.bind("<Key>", createListAuteur)
	entreeAuteur.grid(row=r,column=1, sticky=W+E)
	entreeAuteur.focus_set()
	
	r += 1
	t2 = Frame(master).grid(row=r)
	text_label = Label(t2, text="Texte :",bg='#535353',fg="white")
	text_label.grid(row=r,column=0, sticky=W)
	textVar=StringVar()
	entreeText = Entry(t2, width=50, textvariable=textVar)
	entreeText.bind('<FocusIn>', playTabSound)
	entreeText.grid(row=r,column=1, columnspan=3, sticky=W+E)	
		
	r += 1	
	t3 = Frame(master).grid(row=r,pady=15)	
	casse = IntVar()
	bouton=Checkbutton(t3, text="Casse", takefocus=False, variable=casse,bg='#535353',activebackground='#535353',fg="#FFFFFF",selectcolor="black")
	bouton.grid(row=r)
	
	Rechercher = Button(t3, text ='Rechercher', command=init2,width=20, fg="white", activebackground='#084B8A', bg='#084B8A')
	Rechercher.grid(row=r,column=1, sticky=E+S)
	
	Afficher = Button(master,width=20, compound=LEFT, overrelief=GROOVE, text ='Afficher', fg="red", command=afficherRecherche, state=DISABLED)
	Afficher.grid(row=r,column=2, sticky=W+S)
	
	Aide = Button(master,compound=LEFT, overrelief=GROOVE, text ='?', font=("Arial", 10, "bold"), bg="#4B4242", fg="#F7EF04", command=windowsHelp)
	Aide.grid(row=r,column=3, sticky=E+W+S)
	
	r += 1
	t3a = Frame(master).grid(row=r,sticky=N)
	image = IntVar()
	bouton2=Checkbutton(t3a, text="Image", takefocus=False, variable=image,bg='#535353',activebackground='#535353',fg="#FFFFFF",selectcolor="black",	command=testButtonImg)
	bouton2.grid(row=r)
	
	Delete = Button(t3a,width=20, text ='Supprimer l\'archivage', fg="white", activebackground='#8A0808', bg='#8A0808', command=deleteSujet)
	Delete.grid(row=r,column=1, columnspan = 2)
	
	Raccourci = Button(t3a, text ='R', fg="black", activebackground='white', bg='white', command=determineRacc)
	Raccourci.grid(row=r,column=3)
	
	t3a = Frame(master).grid(pady=15)
	
	r += 1
	t3b = Frame(master).grid(row=r,sticky=N)
	video = IntVar()
	bouton3=Checkbutton(t3b, text="Video", takefocus=False, variable=video,bg='#535353',activebackground='#535353',fg="#FFFFFF",selectcolor="black",	command=testButtonVid)
	bouton3.grid(row=r)
	
	DeleteSearch = IntVar()
	bouton4=Button(t3b,width=20, text ='Nouvelle recherche', fg="white", activebackground='#088A08', bg='#088A08', command=nelleRech)
	bouton4.grid(row=r,column=1, columnspan = 2)
	
	SoundVar = IntVar(value=1)
	sound=Checkbutton(t3b, text="♫", takefocus=False, variable=SoundVar,bg='#535353',activebackground='#535353',fg="#FFFFFF",selectcolor="black")
	sound.grid(row=r,column=2, sticky=S+E)

	MAJVar = IntVar(value=online)
	maj=Checkbutton(t3b, text="@", takefocus=False, variable=MAJVar,bg='#535353',activebackground='#535353',fg="#FFFFFF",selectcolor="black")
	maj.grid(row=r,column=2, padx=50, sticky=S+E)
	maj.bind("<ButtonRelease-1>", changeParams)
	
	r += 1
	t4 = Frame(master).grid(row=r)
	pCurrent = Progressbar(t4, orient='horizontal', mode='determinate', value=5, maximum=nbOfPages)
	pCurrent.grid(row=r, column=0,columnspan=4, sticky=W+E)	
	
	r += 1
	t5 = Frame(master).grid(row=r)
	scrollbar = Scrollbar(t5)
	scrollbar.grid(row=r, column=3,sticky=W+S+N+E)
	texto = Text(t5, wrap=WORD, yscrollcommand=scrollbar.set, width=50, height=15, cursor='heart')
	texto.grid(row=r,column=0, columnspan=3, sticky=W+E)
	scrollbar.config(command=texto.yview)
	

threading.Timer(5, testConnexion).start()
fenetre()

master.deiconify() 	
master.mainloop()
	
	
