import Tkinter as tk
from Tkinter import *
import time
import threading
import Queue
import os.path as path


class GuiPart:
	domain = {'Allergies':0, 'Assessment':0,'Family_History':0,'HPI':0,\
			'Medical_History':0, 'Medications':0, 'Patient_Instructions':0,\
			'Physical_Exam':0,'Plan':0,'Review_of_Systems':0}
	config = {'Allergies':[1,0,0,0],'Assessment':[],'Family_History':[],'HPI':[],\
			'Medical_History':[], 'Medications':[], 'Patient_Instructions':[],\
			'Physical_Exam':[],'Plan':[],'Review_of_Systems':[]}

	def DrawTextBox(self,config,category,text):
		label = tk.Label(self.master,text=category)
		label.grid(row=start_row,column=start_column)
		self.domain['category'] = tk.Text(self.master,wrap="word",width=30,height=4,font="Helvetica, 10")
		text = category + "will go here."
		self.domain['category'].insert(END,text)
		self.domain['category'].grid(row= start_row+1,column=start_column)

	def DrawListBox(self,column_in,category):
		label = tk.Label(self.master,text=category)
		label.grid(row=1,column=0)
		contents = (category,'goes','here')
		list_var = tk.StringVar(value=contents)
		self.domain[category] = tk.Listbox(self.master, listvariable=list_var)
		self.domain[category].grid(row=2,column=column_in,rowspan=4)
	
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
		self.DrawListBox(0,'Medications')

		# Allergies
		self.DrawListBox(1,'Allergies')

		# Family History
		self.DrawListBox(2,'Family_History')

		# Medical History
		self.DrawTextBox(6,0,'Medical_History')
		
		# History of Present Illness (HPI)
		self.DrawTextBox(8,0,'Review_of_Systems')

		# Review of Systems (ROS)
		self.DrawTextBox(10,0,'Review_of_Systems')

		# Physical Exam
		self.DrawTextBox(12,0,'Physical_Exam')

		# Assessment
		self.DrawTextBox(12,2,'Assessment')

		# Plan
		self.DrawTextBox(14,0,'Plan')

		# Patient Instructions
		self.DrawTextBox(14,2,'Patient_Instructions')

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
