import Tkinter as tk
from Tkinter import *
import time
import threading
import Queue
import os.path as path
import datetime
import sklearn.datasets
from sklearn.datasets import load_files
import sklearn.metrics
import sklearn.svm
import sklearn.naive_bayes
import numpy as np
from sklearn.naive_bayes import MultinomialNB
import sklearn.neighbors
import sys, os, glob, operator
from pprint import pprint
import plac
import spacy, scipy
from numpy import ravel
import numpy as np
from spacy import displacy
import en_core_web_sm
from sklearn import svm
nlp = en_core_web_sm.load()

FAMILY_LIST = ['father', 'mother', 'parent', 'mom', 'dad', 'son', 'daugther',
			   'sister', 'brother', 'uncle', 'aunt', 'grandpa', 'grandma', 'grandfather',
			   'grandmother', 'grandparents', 'cousin', 'neice', 'uncle', 'aunt'
				]




def Allergies_Parse(phrase):
	# We just need to get allergen
	print("Nlp part for Allergies:")
	doc = nlp(unicode(phrase))
	allergen = 'allergen'
	keywords = []

	keywords = []

	for token in doc:
		if token.dep_ == 'dobj' or token.dep_ == 'pobj' and not token.is_stop:
			keywords.append(token.text)
		elif token.dep_ == 'nsubj' and token.pos_ == 'NOUN':
			keywords.append(token.text)

	return keywords


	# allergen_flag = 1
	#
	# for count, token in enumerate(doc):
	# 	# print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
	# 	if token.dep_ == 'pobj':
	# 		allergen = token
	# 		allergen_flag = 0
	#
	# if allergen_flag:
	# 	for token in doc:
	# 		if token.pos_ == 'NOUN' and token.dep_ == 'nsubj':
	# 			allergen = token
	#
	# return str(allergen)




def Assessment_Parse(phrase):
	# Recognize terms for medical conditions / diagnoses.
	# Just find final assessment

	print("Nlp part for Assessment:")
	nlp = spacy.load('en')
	doc = nlp(phrase)
	condition = 'condition'
	condition_flag = 1

	keywords = []

	for token in doc:
		if not token.is_stop:
			if token.dep_ == 'dobj' or token.dep_ == 'pobj':
				keywords.append(token.text)
			elif token.tag_ == 'VBG':
				keywords.append(token.text)
	return keywords

	#
	# for count, token in enumerate(doc):
	# 	if token.dep_ == 'dobj':
	# 		condition = token
	# 		condition_flag = 0
	# 	elif token.dep_ == 'pobj':
	# 		condition = token
	# 		condition_flag = 0
	#
	# if condition_flag:
	# 	for token in doc:
	# 		if token.pos_ == 'NOUN' and token.dep_ == 'nsubj':
	# 			condition = token
	#
	# return str(condition)

def FamilyHistory_Parse(phrase):
	# We need to capture condtion and the family member


	print("Nlp part for Family History:")

	nlp = spacy.load('en')
	doc = nlp(unicode(phrase))

	keywords = []

	for token in doc:
		if not token.is_stop:
			if token.dep_ == 'dobj' or token.dep_ == 'pobj' or token.dep_ == 'nsubj':
				keywords.append(str(token))
			elif token.tag_ == 'VBG':
				keywords.append(token.text)
	return keywords
	# # This is used to see if there is a family member from our list

	# condition = 'condition'
	# fam_relation = 'family relation'
	#
	# fam_flag = 1
	# for word in doc:
	# 	if str(word) in FAMILY_LIST:
	# 		fam_flag = 0
	# 		fam_relation = word
	#
	#
	#
	# # Family members tend to be the subject noun of the sentence
	# # The condition tends to be the direct object.
	# for count, token in enumerate(doc):
	# 	# print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
	# 	if token.dep_ == 'dobj':
	# 		condition = token
	# 	elif fam_flag == 1 and token.pos_ == 'NOUN' and token.dep_ == 'nsubj':
	# 		fam_relation = token
	#
	# return str(condition), str(fam_relation)

def HPI_Parse(phrase):
	# Just get the conditions and symptoms from patient
	# Also capture the duration

	print("Nlp part for HPI:")

	doc = nlp(phrase)
	condition = 'condition'
	duration = 'duration'

	keywords = []

	for token in doc:
		if not token.is_stop:
			if token.dep_ == 'dobj' or token.dep_ == 'pobj' or token.dep_ == 'nsubj':
				keywords.append(token.text)
			elif token.pos_ == 'ADJ' and token.pos_ == 'NOUN':
				keywords.append(token.text)
			elif token.tag_ == 'VBG':
				keywords.append(token.text)
	return keywords
	#
	# for count, token in enumerate(doc):
	# 	# print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
	# 	if token.dep_ == 'dobj':
	# 		condition = token
	# 	if token.dep_ == 'pobj' and doc[count - 1].dep_ == 'prep':
	# 		condition = token
	# 	last_word = token
	#
	# for ent in doc.ents:
	# 	# print(ent.text, ent.start_char, ent.end_char, ent.label_)
	# 	if ent.label_ == 'DATE':
	# 		duration = ent.label_

	# if str(duration) == 'duration' and str(condition) == 'condition':
	# 	return
	# elif str(duration) != 'duration' and str(condition) == 'condition':
	# 	return str(duration)
	# elif str(duration) == 'duration' and str(condition) != 'condition':
	# 	return str(duration)
	# else:
	# 	return str(condition), str(duration)


def MedicalHistory_Parse(phrase):
	# Recognize conditions and diagnoses from past


	print("Nlp part for Medical History:")

	doc = nlp(phrase)
	MedHis = 'Medical History'
	compound_flag = 0
	keywords = []

	for token in doc:
		if not token.is_stop:
			if token.dep_ == 'dobj' or token.dep_ == 'pobj':
				keywords.append(token.text)

	return keywords
	#
	# for count, token in enumerate(doc):
	# 	if count >= 1:
	# 		if doc[count -1].dep_ == 'compund' or doc[count -1].dep_ == 'nummound':
	# 			word = str(doc[count -1]) + " " + str(token)
	# 			compound_flag = 1
	# 		else:
	# 			compound_flag = 0
	#
	# 	if token.dep_ == 'dobj':
	# 		MedHis = word if compound_flag == 1 else token
	# 	if token.dep_ == 'pobj' and doc[count - 1].dep_ == 'prep':
	# 		MedHis = word if compound_flag == 1 else token
	#
	# return str(MedHis)

def Medications_Parse(phrase):
	# Recognize medications patient is currently using
	# MIGHT BE A GOOD PLACE FOR A MEDICATIONS ARRAY

	print("Nlp part for Medications:")

	doc = nlp(unicode(phrase))
	Meds = 'Medication'
	compound_flag = 0

	keywords = []

	for token in doc:
		if not token.is_stop:
			if token.dep_ == 'dobj' or token.dep_ == 'pobj':
				keywords.append(token.text)

	return keywords

	# for count, token in enumerate(doc):
	# 	if count >= 1:
	# 		if doc[count -1].dep_ == 'compund' or doc[count -1].dep_ == 'nummound':
	# 			word = str(doc[count -1]) + " " + str(token)
	# 			compound_flag = 1
	# 		else:
	# 			compound_flag = 0
	#
	# 	if token.dep_ == 'dobj':
	# 		Meds = word if compound_flag == 1 else token
	# 	if token.dep_ == 'pobj' and doc[count - 1].dep_ == 'prep':
	# 		Meds = word if compound_flag == 1 else token
	#
	# return str(Meds)

def PatientInstructions_Parse(phrase):
	# Just pass whole sentence

	return str(phrase)

	pass
def PhysicalExam_Parse(phrase):
	# Recognize terms for conditions that can be identified during physical exam
	# GOOD PLACE TO PUT IN A LIST OF PHYSCIAL EXAMS
	# nchunk = list(doc.noun_chunks)
	# for x in nchunk:
	# 	print(x)
	keywords = []
	doc = nlp(phrase)

	nchunk = list(doc.noun_chunks)

	for chunk in nchunk:
		if chunk.root.dep_ == 'dobj' or chunk.root.dep_ == 'pobj':
			keywords.append(chunk.text)

	for token in doc:
		if not token.is_stop:
			if token.pos_ == 'ADJ':
				keywords.append(token.text)

	return keywords


def Plan_Parse(phrase):
	# * Recognize lab tests and automate ordering.
	# * Recognize prescriptions and automate ordering.
	# * Record action items as sentences and ask if they should be added to the plan.


	print("Nlp part for Plan:")

	doc = nlp(phrase)
	PhysExam = 'Physical Exam'
	compound_flag = 0

	keywords = []

	for token in doc:
		if not token.is_stop:
			if token.dep_ == 'dobj' or token.dep_ == 'pobj':
				keywords.append(token.text)

	return keywords

	# for count, token in enumerate(doc):
	# 	if count >= 1:
	# 		if doc[count -1].dep_ == 'compund' or doc[count -1].dep_ == 'nummound':
	# 			word = str(doc[count -1]) + " " + str(token)
	# 			compound_flag = 1
	# 		else:
	# 			compound_flag = 0
	#
	# 	if token.dep_ == 'dobj':
	# 		PhysExam = word if compound_flag == 1 else token
	# 	if token.dep_ == 'pobj' and doc[count - 1].dep_ == 'prep':
	# 		PhysExam = word if compound_flag == 1 else token
	#
	# return str(PhysExam)


def ReviewOfSystems_Parse(phrase):
	# Recognize terms provided is ROS doc and synonyms
	# Make a list from the ROS document

	keywords = []

	for token in doc:
		if not token.is_stop:
			if token.dep_ == 'dobj' or token.dep_ == 'pobj' or token.pos_ == 'ADJ':
				keywords.append(token.text)
			elif token.tag_ == 'VBG':
				keywords.append(token.text)

	return keywords
def ReviewOfSystems_Parse(phrase):
    # Recognize terms provided is ROS doc and synonyms
    # Make a list from the ROS document

    keywords = []

    for chunk in (phrase.noun_chunks):
        if chunk.root.dep_ == 'dobj' or chunk.root.dep_ == 'pobj':
            keywords.append(chunk.text)

    return keywords

class GuiPart:
	domain = {'Allergies':0, 'Assessment':0,'Family_History':0,'HPI':0,\
			'Medical_History':0, 'Medications':0, 'Patient_Instructions':0,\
			'Physical_Exam':0,'Plan':0,'Review_of_Systems':0}

	# value of configs is an array that stores [row,column,rowspan,columnspan]
	configs = {'Allergies':[1,1,4,0],'Assessment':[12,2,0,2],\
			'Family_History':[1,2,4,0],'HPI':[8,0,0,4],\
			'Medical_History':[6,0,0,4], 'Medications':[1,0,4,0], \
			'Patient_Instructions':[14,2,0,2],'Physical_Exam':[12,0,0,2],\
			'Plan':[14,0,0,2],'Review_of_Systems':[10,0,0,4]}

	def DrawBox(self,category,textin):
		config = self.configs[category]
		label = tk.Label(self.master,text=category)
		label.grid(row=config[0],column=config[1])
		if(category == 'Medications' or category == 'Allergies' or category == 'Family_History'):
			#Listbox
			contents = (textin)
			list_var = tk.StringVar(value=contents)
			self.domain[category] = tk.Listbox(self.master, listvariable=list_var)
			self.domain[category].grid(row=config[0]+1,column=config[1],rowspan=config[2])
		else:
			#Textbox
			self.domain[category] = tk.Text(self.master,wrap="word",width=30,height=4,font="Helvetica, 10")
			text = textin
			self.domain[category].insert(END,text)
			self.domain[category].grid(row= config[0]+1,column=config[1],columnspan = config[3])
		
	
	def __init__(self, master, queue, initial, endCommand):
		self.queue = queue
		self.master = master
		self.initial = initial
		# Set up the GUI
		#console = tk.Button(master, text='Done', command=endCommand)
		#console.pack()
		# Add more GUI stuff here
		textin = "..."
		master.title("Electronic Medical Record")
		master.grid()
		name = tk.Label(master,text="Jane Doe", font="Arial 16 bold")
		age = tk.Label(master,text="27 years old")
		gender = tk.Label(master,text="Female")
		name.grid(row=0,column=0)
		age.grid(row=0,column=1)
		gender.grid(row=0,column=2)
		button = tk.Button(master, text='Exit', command=endCommand)
		button.grid(row=0,column=3)
		buttong = tk.Button(master, text = 'Generate', command = self.generate)
		buttong.grid(row=0,column = 4)
		for category in self.domain.keys():
			self.DrawBox(category,textin)

	def createDialog(self, keywords, category):
		dialog = Toplevel(self.master)
		dialog.grid()
		dialog.title("Add to EMR")
		label = tk.Label(dialog,text="Add: ")
		label.grid(row=1,column=0)
		entry = tk.Entry(dialog,width = 60000000)
		entry.insert(END,keywords)
		entry.grid(row=1,column=1)
		label = tk.Label(dialog,text=" to ")
		label.grid(row=1,column=2)
		categories = ("Allergies","Assessment","Family_History","HPI","Medical_History","Medications","Patient_Instructions","Physical_Exam","Plan","Review_of_Systems")
		index = categories.index(category)
		v = tk.StringVar()
		v.set(categories[index])
		categoryMenu = tk.OptionMenu(dialog,v,*categories)
		categoryMenu.grid(row=1,column=3)
		cancelButton = tk.Button(dialog,text="Cancel",command=dialog.destroy)
		cancelButton.grid(row=2,column=2)
		acceptButton = tk.Button(dialog,text="Accept",command=self.addInformation(entry.get(),category))
		acceptButton.grid(row=2,column=3)
		
	def addInformation(self,info,category):
		print("Adding information to "+ category)
		self.DrawTextBox(12,2,category,info)

		
	def createDialog(self, keywords, category):
		dialog = Toplevel(self.master)
		dialog.grid()
		dialog.title("Add to EMR")
		label = tk.Label(dialog,text="Add: ")
		label.grid(row=1,column=0)
		entry = tk.Entry(dialog, width = 45)
		entry.insert(END,keywords)
		entry.grid(row=1,column=1)
		label = tk.Label(dialog,text=" to ")
		label.grid(row=1,column=2)
		categories = ("Medications","Allergies","Family_History","Medical_History",
		"HPI", "Review_of_Systems", "Physical_Exam", "Assessment","Plan","Patient_Instructions")
		index = categories.index(category)
		v = tk.StringVar()
		v.set(categories[index])
		categoryMenu = tk.OptionMenu(dialog,v,*categories)
		categoryMenu.grid(row=1,column=3)
		cancelButton = tk.Button(dialog,text="Cancel",command = dialog.destroy)
		cancelButton.grid(row=2,column=2)
		acceptButton = tk.Button(dialog,text="Accept",command = lambda: self.addInformation(entry.get(),v.get(),dialog))
		acceptButton.grid(row=2,column=3)
		acceptButton = tk.Button(dialog,text="Merge",command = lambda: self.MergeInformation(entry.get(),v.get(),dialog))
		acceptButton.grid(row=2,column=4)

	def addInformation(self,info,category,dialog):
		print(category)
		if(category == 'Medications' or category == 'Allergies' or category == 'Family_History'):
			if(category == "Medications"):
				parseinfo = Medications_Parse(info)
			if(category == "Allergies"):
				parseinfo = Allergies_Parse(info)
			if(category == "Family_History"):
				parseinfo = FamilyHistory_Parse(info)
			#parseinfo = info
			parseinfo = str(parseinfo)
			parseinfo = parseinfo.replace("["," ")
			parseinfo = parseinfo.replace("]"," ")
			parseinfo = parseinfo.replace("u'"," ")
			parseinfo = parseinfo.replace("'"," ")
			parseinfo = parseinfo.replace(","," ")




			temp = self.domain[category]
			print(temp)
			temp = temp.get(0,END)
			#temp = temp[0]
			temp = str(parseinfo)

		else:
			temp = self.domain[category]
			print(temp)
			temp = temp.get("1.0",END)
			parseinfo = info + "  ;  "
			temp = str(temp) + "    "+ str(parseinfo)

		print parseinfo
		self.DrawBox(category,temp)
		dialog.destroy()

	def MergeInformation(self,info,category,dialog):
		print(category)
		if(category == 'Medications' or category == 'Allergies' or category == 'Family_History'):
				temp = self.domain[category]
				print(temp)
				temp = temp.get(0,END)
				temp = temp[0]
		else:
				temp = self.domain[category]
				print(temp)
				temp = temp.get("1.0",END)
		info = info.split(':')
		info = info[1]
		temp = temp + " "+ info
		self.DrawBox(category,temp)
		dialog.destroy()
	def generate(self):
		categories = ("Allergies","Assessment","Family_History","HPI","Medical_History","Medications","Patient_Instructions","Physical_Exam","Plan","Review_of_Systems")
		html = "<!DOCTYPE html><html><head><meta charset = \"utf-8\"><title>EMR Table</title><link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\"></head><br><br><br><div id =\"Etable\"><table id = \"EMRTable\"><caption>Electrical Medical Record</caption><tr><th>Category</th><th>Content</th></tr>"
		htmlw = "./EMRresult.html"
		currenttime = datetime.datetime.now()
		currenttime = ''.join(["Date:",str(currenttime)])
		htmlw = "./EMRresult"+currenttime+".html"
		print(self.domain["Medications"].get(0,END),self.domain["HPI"].get("1.0",END))
		f = open(htmlw,'w')
		for i in range(0,10):
			print(categories[i])
			if(categories[i] == 'Medications' or categories[i] == 'Allergies' or categories[i] == 'Family_History'):
				temp = self.domain[categories[i]]
				print(temp)
				temp = temp.get(0,END)
			else:
				temp = self.domain[categories[i]]
				print(temp)
				temp = temp.get("1.0",END)



			currenttime = datetime.datetime.now()
			currenttime = ''.join(["Date:",str(currenttime)])
			filename = "./trainingdata/"+categories[i]+"/"+currenttime+".txt"	
			trainingfile = open(filename,"w")
			trainingfile.write(str(temp))
			trainingfile.close
			print ("(Training Data) Writing ",str(temp)," to ",categories[i])
			html = html + "<tr><td>" + categories[i]+ "</td><td>" + str(temp) + "</td></tr>"
		html = html + "</table></div></body></html>"
		f.write(html)
		f.close()



	'''
	def generate(self):
		print("Generating EMR page and training data")
    	currenttime = datetime.datetime.now()
    	currenttime = ''.join(["Date:",str(currenttime)])
    	filename = ''.join([currenttime,".txt"])
    	fullfilename = ''.join([self.meds_var,"/",filename])
    	trainingfile = open(fullfilename,"w")
    	trainingfile.write(text)
    	trainingfile.close
	'''

	def processIncoming(self):
		"""
		Handle all the messages currently in the queue (if any).
		"""
		while self.queue.qsize():
			try:
				msg = self.queue.get(0)
				# Check contents of message and do what it says
				# As a test, we simply print it
				f = open('./data/text.txt','r')
				current = f.readlines()
				if current != self.initial:
					for line in current:
						if line not in self.initial:
							print(line.partition(','))
							if (line != None) and (line != '') and (line != '\n'):
								info = line.partition(',')
								self.createDialog(info[0],info[2].replace('\n',''))
					self.initial = current
				else:
					print('file not modified')
				print msg
			except Queue.Empty:
				pass

class ThreadedClient:
	"""
	Launch the main part of the GUI and the worker thread. periodicCall and
	endApplication could reside in the GUI part, but putting them here
	means that you have all the thread controls in a single place.
	"""
	def __init__(self, master):
		"""
		Start the GUI and the asynchronous threads. We are in the main
		(original) thread of the application, which will later be used by
		the GUI. We spawn a new thread for the worker.
		"""
		self.master = master

		# Create the queue
		self.queue = Queue.Queue()

		# Set up the GUI part
		f = open('./data/text.txt','r')
		initial = f.readlines()
		self.gui = GuiPart(master, self.queue, initial, self.endApplication)

		# Set up the thread to do asynchronous I/O
		# More can be made if necessary
		self.running = 1
		self.thread1 = threading.Thread(target=self.workerThread1)
		self.thread1.start()

		# Start the periodic call in the GUI to check if the queue contains
		# anything
		self.periodicCall()

	def periodicCall(self):
		"""
		Check every 100 ms if there is something new in the queue.
		"""
		self.gui.processIncoming()
		if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
			import sys
			sys.exit(1)
		self.master.after(100, self.periodicCall)

	def workerThread1(self):
		"""
		This is where we handle the asynchronous I/O. For example, it may be
		a 'select()'.
		One important thing to remember is that the thread has to yield
		control.
		"""
		while self.running:
			# To simulate asynchronous I/O, we create a random number at
			# random intervals. Replace the following 2 lines with the real
			# thing.
			time.sleep(2)
			msg = "checking..."
			self.queue.put(msg)

	def endApplication(self):
		self.running = 0


root = tk.Tk()

client = ThreadedClient(root)
root.mainloop()
