# -*- coding: utf8 -*-
import webbrowser
from urllib.request import urlopen, urlretrieve
import unidecode
import threading
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import os, shutil
import time
import winsound
from pyunpack import Archive
import winshell
from win32com.client import Dispatch
 
master=Tk()
master.withdraw()
master.configure(background='#535353')
master.title("Véganisme - Rechercher / Koreus.com (v.3.5.6)")

###########
#VARIABLES#
###########
global derTxt, texto, o, bar
nbOfPages = 225
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
	pageTest=urlopen('https://www.koreus.com/modules/newbb/topic160787.html') 
	strpageTest=pageTest.read().decode('utf-8')
	splitText = '''<b>(1)</b> <a href="/modules/newbb/topic160787-20.html">2</a> <a href="/modules/newbb/topic160787-40.html">3</a> <a href="/modules/newbb/topic160787-60.html">4</a> ... <a '''
	listSST = strpageTest.split(splitText)
	listEST = listSST[1].split("</a>")
	listNSST = listEST[0].split(">")
	nbOfPages = int(listNSST[1])

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
	file.close()
	print('Bug 1')
	
######################
# DELETE OLD VERSION #
######################	
if online:
	try:
		urlHost = 'http://hostmajveganisme1.e-monsite.com/'
		page=urlopen(urlHost)
		strpage=page.read().decode('utf-8')
		lastMAJ=strpage[strpage.index('<li><strong>Nom du fichier : </strong>')+len('<li><strong>Nom du fichier : </strong>'):strpage.index('</li>')]
		linkMAJ=strpage[strpage.index('<a href="')+len('<a href="'):strpage.index('" title="')]
		fullPath =  chemin+"\\"+lastMAJ
	except:
		fullPath = "INACESSIBLE"
		print('Bug 2')

def createShortCut():
	desktop = winshell.desktop()	
	path = os.path.join(desktop, "Veganisme.lnk")
	target = fullPath+"\\"+lastMAJ+".exe"
	wDir = fullPath
	icon = fullPath+"\\"+lastMAJ+".exe"
	if not os.path.exists(path): 
		shell = Dispatch('WScript.Shell')
		shortcut = shell.CreateShortCut(path)
		shortcut.Targetpath = target
		shortcut.WorkingDirectory = wDir
		shortcut.IconLocation = icon
		shortcut.save()

def download():
	global o
	urlretrieve(linkMAJ, chemin+"\\"+lastMAJ+".zip")	
	Archive(chemin+"\\"+lastMAJ+".zip").extractall(chemin)
	os.remove(chemin+"\\"+lastMAJ+".zip")
	bar.stop()
	bar['mode']='determinate'
	bar['value']=100
	os.startfile(fullPath+"\\"+lastMAJ+".exe")
	
def oExit():
	global o
	o.destroy()

if online:
	if fullPath != "INACESSIBLE":
		if not os.path.exists(fullPath):
			print('DOESNT EXIST')
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
			bar = Progressbar(o, orient='horizontal', mode='indeterminate', length=200, maximum=100)
			bar.grid(row=1, column=0, sticky=W+E)
			OK = Button(o, overrelief=GROOVE, text ='OK', command=oExit)
			OK.grid(row=2)
			bar.start(1)
			o.mainloop()
		
	listDir = os.listdir(chemin)
	for dir in listDir:
		if dir.startswith("webRead") and dir.lower()!=lastMAJ.lower():
			shutil.rmtree(chemin+'\\'+dir)
			
	if fullPath != "INACESSIBLE":
		createShortCut()	

def windowsAlert():
	windowsAnswer = messageBox.askyesno("Continuer?", "Le script va supprimer toutes les archives permettant la recherche, voulez vous continuer?")
	return windowsAnswer
	
def windowsHelp():
	messageBox.showinfo("Aide", "Raccourcis :\n\
- Tabulation pour naviguer sans souris\n\
- Entrée pour lancer la recherche\n\
- * dans la zone auteur pour sélectionner tous les auteurs\n\
Boutons :\n\
- Casse : Prendre en compte les accents et majuscules\n\
- Image : Non-disponible pour le moment\n\
- Video : Recherche uniquement les vidéos\n\
- Rechercher : Lance la recherche\n\
- Supprimer l'archivage : Permet de supprimer les archives Str, Videos et Images. \
Il est conseillé de le faire après une mise à jour!\n\
- Nouvelle recherche : Supprime les paramètres de recherche saisis.\n")
	
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
	
	list = file.split("#aut]\n\n")
	for line in list[:-1]:		
		try: #line commentaire
			comstr = line[line.index("[#coms:\n")+8:line.index("#coms]\n\n\n")]
			coms = comstr.split("#---------------------------------------------------------------------\n")	
			for com in coms:
				page = com[com.index('#Page:')+6:com.index('\n#ForumPost:')]
				if type == 'str':
					fp = com[com.index('#ForumPost:')+11:com.index('\n#Text:')]
					comm = com[com.index('#Text:')+6:-1]
					dico[auteur].extend([page,fp,comm])
				elif type == 'img':
					fp = com[com.index('#ForumPost:')+11:com.index('\n#Image:')]
					img = com[com.index('#Image:')+7:-1]
					dicoImg[auteur].extend([page,fp,img])
				elif type == 'vid':
					fp = com[com.index('#ForumPost:')+11:com.index('\n#Video:')]
					vid = com[com.index('#Video:')+7:-1]
					dicoVid[auteur].extend([page,fp,vid])
		except:
			auteur = line[line.index("[#aut:")+6:]
			for a in accents2:
				auteur = auteur.replace(a[0],a[1])
				if type == 'str':
					dico[auteur]=[]
				elif type == 'img':
					dicoImg[auteur]=[]
				elif type == 'vid':
					dicoVid[auteur]=[]
					
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
					if listCom[countComm]+"##" not in dico[auteur]:
						dico[auteur].extend([str(suf[countPage]),listCom[countComm]+"##",h02])
				else:
					dico[auteur]=[str(suf[countPage]),listCom[countComm]+"##",h02]
				
				count = 0
				for img in imgs:	
					if auteur in dicoImg:
						if listCom[countComm]+'-'+str(count) not in dicoImg[auteur]:
							dicoImg[auteur].extend([str(suf[countPage]),listCom[countComm]+'-'+str(count),img])
					else:
						dicoImg[auteur]=[str(suf[countPage]),listCom[countComm]+'-'+str(count),img]
					count+=1

				count=0
				for vid in vids:
					if auteur in dicoVid:
						if listCom[countComm]+'-'+str(count) not in dicoVid[auteur]:
							dicoVid[auteur].extend([str(suf[countPage]),listCom[countComm]+'-'+str(count),vid])
					else:
						dicoVid[auteur]=[str(suf[countPage]),listCom[countComm]+'-'+str(count),vid]
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
			page = False
			fp = False			
			for obj in dic[auteur]:
				if not page:				
					file.write("#Page:"+obj+"\n")
					if int(obj)>int(biggestPage):
						biggestPage=obj
					page = True
					continue
				if not fp:
					file.write("#ForumPost:"+obj+"\n")
					fp = True
					continue
				if page and fp:
					if dics.index(dic) == 0:
						file.write("#Text:"+obj+"\n")
					elif dics.index(dic) == 1:
						file.write("#Image:"+obj+"\n")					
					elif dics.index(dic) == 2:
						file.write("#Video:"+obj+"\n")
					file.write("#---------------------------------------------------------------------\n")					 
					page = False
					fp = False
					
		
			file.write("#coms]\n\n\n")
		file.write("\n"+str(lastLenPage)+"-"+biggestPage)
		file.close()
	
def rechercher():
	#ENREGISTRE LE SUJET/MET A JOUR L'ARCHIVAGE/RECHERCHE L'EXTRAIT DU TEXTE EN FONCTION DE L'AUTEUR
	global listCom, dico, texto, derTxt, research_thread, lastPage, dicoImg, dicoVid
	if online:
		lastPage=int(nbOfPages)*20 #LAST PAGE + (1*20)
	
	#PREMIERE UTILISATION (CREATION DES ARCHIVES SUR LE DISQUE DUR)
	filesName = ["Sujet.txt","Images.txt","Videos.txt"]
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
			break #dicoAnWriteStr écrit les 3 dictionnaires et les fichiers correspondants
		
	#ARCHIVAGE DEJA EXISTANT
	else:
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
	global listResult, dico, texto, derTxt, result, entree2, auteur2	
	#RECHERCHER PAR AUTEUR L'EXTRAIT
	try:
		derTxt = "\n"+"RECHERCHE EN COURS..."
		texto.insert(END, derTxt)
		
		pCurrent['mode'] = "indeterminate"
		pCurrent.start(1)
		listResult = []
		result = 0
		if image.get():
			dic = dicoImg
		elif video.get():
			dic = dicoVid
		else:
			dic = dico
		keys = []
		for key in dic.keys():
			keys.append(key.lower())

		for auteur in auteur2:
			if auteur not in keys:
				derTxt = "\n"+auteur+" AUTEUR NON TROUVE"
				texto.insert(END, derTxt)
				continue
				
			for key in dic.keys():
				if auteur in key.lower():
					auteur = key
					
			for comm in dic[auteur]:

				try:
					if int(comm)<200000:
						page = int(comm)
				except:
					None
				try:
					if int(comm[:-2])>200000:
						num = comm[:-2]							
				except:
					None
				try:						
					comm1 = comm
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
						if mot in comm2 and len(comm.split())>1:								
							listMotInComm.append(comm2.index(mot))								
							motPresent = True
							countMot = comm2.count(mot)
							if casse.get():
								idOpenSpan = comm.index(mot)
								idCloseSpan = idOpenSpan+len(mot)
								listIdSpan.append([idOpenSpan,idCloseSpan])
							else:
								idOpenSpan = comm2.index(mot)
								idCloseSpan = idOpenSpan+len(mot)
								listIdSpan.append([idOpenSpan,idCloseSpan])

					if motPresent:
						
						for list in listIdSpan[::-1]:
							comm = comm[:list[1]]+"</span>"+comm[list[1]:]
							comm = comm[:list[0]]+'<span style="background-color: #DA81F5;" >'+comm[list[0]:]						
	
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
							listResult.insert(idInsert,[page,num,comm,auteur,points])
						else:
							listResult.append([page,num,comm,auteur,points])
						
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

def buildPageWeb(aff=False):
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
		if result >= 200 and not aff:
			derTxt=""
			texto.delete(1.0, END)
			derTxt = "\n"+"Nombre de resultats : >200"
			texto.insert(END, derTxt)
			Afficher['state']='normal'
			Afficher['text']='Afficher > 200 résultats'
			Afficher['fg']="red"
			return
			
		if result < 200 and not aff:	
			derTxt = "\n"+"Nombre de resultats : "+str(result)
			texto.insert(END, derTxt)
			Afficher['state']='normal'
			Afficher['text']='Afficher '+str(result)+' résultat(s)'
			Afficher['fg']="#088A08"
			idAfter.append(master.after(250,clignotement))
			return
		
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
		pageWeb.write('''<tr>
		<th colspan="2" style="width:140px;background-color:#9a9ace"><FONT color="#fff">'''+aut+''' - Extrait du texte recherché : '''+entree2+''' - <U>Nombre de résultat(s)</U> : '''+str(result)+'''</FONT></th>
		</tr>''')
	
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
		e = '''<!DOCTYPE html>
		<meta charset="UTF-8">
		<html>
		<table>
		<style>
				table {
					width:100%;
				}
		</style>'''
				
		tdCount = 0
		numPage = 1
		txtPage = calculTxtPage(numPage)
		pageWeb = openPageWeb(numPage, e, txtPage)
		for list in listResult:
			tdCount += 1
			if tdCount == 1:
				pageWeb.write('<tr>\n')				
			pageWeb.write('<td>'+list[2].replace('width=','none').replace('height=','none').replace('>','')+' height=30% width=100% scrolling="no"></iframe><br /><a href="https://www.koreus.com/modules/newbb/topic160787-'+str(list[0])+'.html#forumpost'+str(list[1])+'"> Page '+str((int(list[0])+20)/20)+' / ForumPost.'+str(list[1])+'</a></td>\n')
			#<iframe src="https:www.youtube.com/embded/xxxxx1" frameborder=0  height=30% width=100% scrolling="no"></iframe>
			if tdCount % 3 == 0:
				pageWeb.write('</tr>\n')
			if tdCount % 12 == 0 and numPage != lastPage:
				pageWeb.write("</table>")
				numPage += 1
				txtPage = calculTxtPage(numPage)				
				pageWeb.close()	
				pageWeb = openPageWeb(numPage, e, txtPage)
				tdCount = 0
		pageWeb.write('</table>')
		pageWeb.close()
		displayPageWeb = threading.Thread(target=displaySearch,args=("vid",))
					
	if image.get():
		derTxt = "\n"+"Fonctionnalité non développée pour le moment"
		texto.insert(END, derTxt)	
		
	displayPageWeb.daemon = True
	displayPageWeb.start()

def calculTxtPage(numPage):
	if float(result)/12 > (result)/12:
		lastPage = ((result)/12)+1
	else:
		lastPage = ((result)/12)
	c = 1
	txtPage = "Page : "
	while lastPage >= c:
		if c == numPage:
			txtPage += "<a href=file:///"+chemin+"\\pageWeb"+str(c)+".html"+"><font color='#8A084B'>("+str(c)+") </font></a>   "
		else:
			txtPage += "<a href=file:///"+chemin+"\\pageWeb"+str(c)+".html"+">"+str(c)+" </a>   "
		c += 1
	return txtPage
	
def openPageWeb(count, e, txtPage):
	pageWeb = open(chemin+"\\pageWeb"+str(count)+".html","w")
	pageWeb.write(e)
	try:
		aut = unidecode.unidecode(entreeAuteur.get())
	except:
		aut = entreeAuteur.get()
	aut = aut.replace(";"," ")
	pageWeb.write('<tr><th colspan="3" style="width:140px;background-color:#9a9ace"><FONT color="#fff">'+aut+' - Extrait du texte recherché : '+entree2+' - <U>Nombre de résultat(s)</U> : '+str(result)+'</FONT></th></tr>\n')
	pageWeb.write('<tr><th colspan="3" style="width:140px;background-color:#9a9ace">'+txtPage+'</th></tr>')
	return pageWeb

def displaySearch(argu):
	if not result:
		return
	if argu == "str":
		os.startfile("C:/Users/LeNa/Veganisme/pageWeb.html")

	elif argu == "vid":
		os.startfile("C:/Users/LeNa/Veganisme/pageWeb1.html")

	#Afficher['state']='disabled'
	
def testButtonImg():
	global ideo, bouton3
	if image.get():
		video.set(0)
		image.set(0)
		texto.delete(1.0, END)
		derTxt = "\n"+"Fonctionnalité non développée pour le moment"
		texto.insert(END, derTxt)

def testButtonVid():	
	global image, bouton2
	if video.get():
		image.set(0)
		texto.delete(1.0, END)
	
def init2(evt=1):
	global search_thread, derTxt, texto, entree2, auteur2
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
	if len(entreeText.get())<5 and not image.get() and not video.get():
		if SoundVar.get():
			winsound.Beep(500,50)
			winsound.Beep(300,50)
		derTxt = "\n"+"L'EXTRAIT DE TEXTE EST TROP COURT (MIN 5 CARACTERES)"
		texto.insert(END, derTxt)
		return		
	auteur = entreeAuteur.get() #Unicode si accent, string sinon
	auteurs = auteur.split(";")
	while "" in auteurs:
		auteurs.remove("")
	auteur2 = []
	for auteur in auteurs:
		try:
			auteur2.append(unidecode.unidecode(auteur.lower()))
		except:
			auteur2.append(auteur.lower())
		
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
	buildPageWeb(True)
	
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
	else: #Permet de créer value si l'utilisateur n'utilise pas la liste mais tape directement auteur1;auteur2
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
			listNames = ["-itz-","-JoJo-","-Ninja-","-Stitch-","35445345","_hans","A_Rod","Admonitio","Aethnight","aioren","Alex333","alixoux","alvein","Archib","Arsenick","AshySlashy","Asmodeus","Ataync","Avaruus","benboo","Bend_ua","Biiiiiip","carpet_bombing","Carraidas","Chaoui","Clayton","Cornflake","eck0es","EdTheGrocer","Guillotine","icemelody","Imnothere","Infame_ZOD","Insert","Invite","izard","johnmacjohn","jopopmk","kahlan","Kanchi","Kasanoda","Keussy","Kirouille","Krobot","LaPelle","Leeloochan","LeMat","LeNarvalo","leozero","Leviatan","Loom-","Lorihengrin","maieuh","Marsu_Xp","Mazuru","Miiiichel","Mogliere","MusicMan","Norbert","Olrik","Pam_en_Personne","PandorZz","papives","Petis","PIume","Plopp","posteur","Pouip","Poum45","PPilou","Quokka","raphiol","Rob2017","Rodhar","Simonello","Skara","Skity","Skwatek","Surzurois","Swe_33","THE_ROYE","TheLord","Turlutuutu","Vassili-Zaistev","Vixen","Weedol","Wikiss","Wiliwilliam","WonderSarah","yakow","Zertyy","Zwitterion"]
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
		master.quit()
	elif evt.keycode == nelleKey:
		nelleRech()
	
def getNelleKey(evt):	
	global nelleKey, nleVar
	nelleKey = evt.keycode
	window.after(0,nleVar2,(nleVar))
	file = open(chemin+"\\Raccs.txt","a")
	file.write('NlleRacc :'+str(nelleKey)+'#\n')
	file.close()
	
def nleVar2(var):
	var.set('   [Code Touche : '+str(nelleKey)+']')
	
def getEscapeKey(evt):	
	global escVar,escapeKey
	escapeKey = evt.keycode
	window.after(0,escVar2,(escVar))
	file = open(chemin+"\\Raccs.txt","a")
	file.write('EscRacc :'+str(escapeKey)+'¤\n')
	file.close()
	
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
	
def windowExit():
	global window
	if len(escVar.get())<5 or len(nleVar.get())<5:
		sound_thread = threading.Thread(target=emptyRaccSound)
		sound_thread.daemon = True
		sound_thread.start()		
		blinkWindow()
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
	file = open(chemin+"\\Raccs.txt","w")
	file.write('')
	file.close()
	OK = Button(window, overrelief=GROOVE, text ='OK', command=windowExit)
	OK.grid(row=3,columnspan=2)
	window.overrideredirect(True)
	window.mainloop()

def getAndSetParams():
	global online
	online = MAJVar.get()
	print(online)
	file = open(chemin+"\\Params.txt","w")
	file.write(str(online))
	file.close()

def changeParams(event=1):
	master.after(50,getAndSetParams)
	


def fenetre():
	global Afficher, SoundVar, MAJVar, taped, nameAuteur, texto, pCurrent, entreeAuteur, entreeText, Rechercher, scrollbar, casse, image, video, bouton2, bouton3, textVar
	r = 0
	x = (master.winfo_screenwidth()*0.85 - master.winfo_reqwidth())/2
	y = (master.winfo_screenheight()*0.70 - master.winfo_reqheight())/2
	master.bind('<Return>', init2)
	master.bind('<Key>',testKey)
	master.geometry("+%d+%d" % (x, y))
		
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

fenetre()

master.deiconify() 	
master.mainloop()
	
	
