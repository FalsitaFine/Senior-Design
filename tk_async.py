import Tkinter as tk
from Tkinter import *
import time
import threading
import Queue
import os.path as path


class GuiPart:
	def __init__(self, master, queue, initial, endCommand):
		self.queue = queue
		self.master = master
		self.initial = initial
		# Set up the GUI
		#console = tk.Button(master, text='Done', command=endCommand)
		#console.pack()
		# Add more GUI stuff here
		master.title("Electronic Medical Record")
		master.grid()
		name = tk.Label(master,text="Jane Doe", font="Arial 16 bold")
		age = tk.Label(master,text="27 years old")
		gender = tk.Label(master,text="Female")
		name.grid(row=0,column=0)
		age.grid(row=0,column=1)
		gender.grid(row=0,column=2)
		button = tk.Button(master, text='Done', command=endCommand)
		button.grid(row=0,column=3)
		# Medications
		meds_label = tk.Label(master,text="Medications")
		meds_label.grid(row=1,column=0)
		meds=('Advil','Ibuprophen','Tylenol','Antibiotics')
		meds_var = tk.StringVar(value=meds)
		medications = tk.Listbox(master, listvariable=meds_var)
		medications.grid(row=2,column=0,rowspan=4)

		# Allergies
		label = tk.Label(master,text="Allergies")
		label.grid(row=1,column=1)
		allergies = ('Penicillin')
		allergyList = tk.StringVar(value=allergies)
		allergiesView = tk.Listbox(master, listvariable=allergyList)
		allergiesView.grid(row=2,column=1,rowspan=4)

		# Family History
		label = tk.Label(master,text="Family History")
		label.grid(row=1,column=2)
		famhistory = ('Father - heart condition', 'Mother - diabetes')
		familyHistoryList = tk.StringVar(value=famhistory)
		familyHistoryView = tk.Listbox(master, listvariable=familyHistoryList)
		familyHistoryView.grid(row=2,column=2,rowspan=4)

		# Medical History
		label = tk.Label(master,text="Medical History")
		label.grid(row=6,column=0)
		medicalHistory = tk.Text(master,wrap="word",height=4,font="Helvetica, 10")
		mhtext = "Medical history will go here.  Medical History will go here.  Medical History will go here.  Medical History will go here."
		medicalHistory.insert(END,mhtext)
		medicalHistory.grid(row=7,column=0,columnspan=4)
		
		# History of Present Illness (HPI)
		label = tk.Label(master,text="History of Present Illness (HPI)")
		label.grid(row=8,column=0)
		hpi = tk.Text(master,wrap="word",height=4,font="Helvetica, 10")
		hpiText = "History of Present Illness will go here.  History of Present Illness will go here.  History of Present Illness will go here.  History of Present Illness will go here."
		hpi.insert(END,hpiText)
		hpi.grid(row=9,column=0,columnspan=4)

		# Review of Systems (ROS)
		label = tk.Label(master,text="Review of Systems (ROS)")
		label.grid(row=10,column=0)
		ros = tk.Text(master,wrap="word",height=4,font="Helvetica, 10")
		rosText = "Review of Systems will go here.  Review of Systems will go here.  Review of Systems will go here.  Review of Systems will go here."
		ros.insert(END,rosText)
		ros.grid(row=11,column=0,columnspan=4)

		# Physical Exam
		label = tk.Label(master,text="Physical Exam")
		label.grid(row=12,column=0,columnspan=2)
		pe = tk.Text(master,wrap="word",width=30,height=4,font="Helvetica, 10")
		peText = "Physical Exam Results will go here.  Physical Exam Results will go here.  Physical Exam Results will go here.  Physical Exam Results will go here."
		pe.insert(END,peText)
		pe.grid(row=13,column=0,columnspan=2)

		# Assessment
		label = tk.Label(master,text="Assessment")
		label.grid(row=12,column=2,columnspan=2)
		assessment = tk.Text(master,wrap="word",width=30,height=4,font="Helvetica, 10")
		assessmentText = "Assessment will go here.  Assessment will go here.  Assessment will go here.  Assessment will go here."
		assessment.insert(END,assessmentText)
		assessment.grid(row=13,column=2,columnspan=2)

		# Plan
		label = tk.Label(master,text="Plan")
		label.grid(row=14,column=0,columnspan=2)
		plan = tk.Text(master,wrap="word",width=30,height=4,font="Helvetica, 10")
		planText = "Plan notes will go here.  Plan notes will go here.  Plan notes will go here.  Plan notes will go here."
		plan.insert(END,planText)
		plan.grid(row=15,column=0,columnspan=2)

		# Patient Instructions
		label = tk.Label(master,text="Patient Instructions")
		label.grid(row=14,column=2,columnspan=2)
		pi = tk.Text(master,wrap="word",width=30,height=4,font="Helvetica, 10")
		piText = "Patient instructions will go here.  Patient instructions will go here.  Patient instructions will go here.  Patient instructions will go here."
		pi.insert(END,piText)
		pi.grid(row=15,column=2,columnspan=2)
		
	def createDialog(self, keywords, category):
		dialog = Toplevel(self.master)
		dialog.grid()
		dialog.title("Add to EMR")
		label = tk.Label(dialog,text="Add: ")
		label.grid(row=1,column=0)
		entry = tk.Entry(dialog)
		entry.insert(END,keywords)
		entry.grid(row=1,column=1)
		label = tk.Label(dialog,text=" to ")
		label.grid(row=1,column=2)
		categories = ("Medications","Allergies","Family Medical History","Medical History",
		"HPI", "ROS", "Physical Exam", "Assessment","Plan","Patient Instructions")
		index = categories.index(category)
		v = tk.StringVar()
		v.set(categories[index])
		categoryMenu = tk.OptionMenu(dialog,v,*categories)
		categoryMenu.grid(row=1,column=3)
		cancelButton = tk.Button(dialog,text="Cancel",command=dialog.destroy)
		cancelButton.grid(row=2,column=2)
		acceptButton = tk.Button(dialog,text="Accept",command=self.addInformation(entry.get(),index))
		acceptButton.grid(row=2,column=3)
		
	def addInformation(self,info,category):
		print("Adding information")

	def processIncoming(self):
		"""
		Handle all the messages currently in the queue (if any).
		"""
		while self.queue.qsize():
			try:
				msg = self.queue.get(0)
				# Check contents of message and do what it says
				# As a test, we simply print it
				f = open('text.txt','r')
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
		f = open('text.txt','r')
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
