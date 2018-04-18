'''
import Tkinter
import tkMessageBox

top = Tkinter.Tk()

def helloCallBack():
   tkMessageBox.showinfo( "Hello Python", "Hello World")

B = Tkinter.Button(top, text ="Hello", command = helloCallBack)

B.pack()
top.mainloop()
'''
import time

import Tkinter as tk  
from multiprocessing import Process, Queue, Manager 
import threading
from threading import Thread, current_thread
counter = 0   
def counter_label(label):  
  def count():  
    global counter  
    counter += 1  
    label.config(text=str(counter))  
    label.after(1000, count)  
  count()  
   
def start_UI(title):

	root = tk.Tk()  
	root.title("title")  
	label = tk.Label(root, fg="green")  
	label.pack()  
	counter_label(label)  
	button = tk.Button(root, text='Stop', width=25, command=root.destroy)  
	button.pack()  
	print("UI Start")
	root.mainloop()  
	return 1



'''
p_UI = Process(target = start_UI, args=(root,))
p_UI.start()
'''


t_recog = Process(target = start_UI, args = ("root",))
t_recog.start()


print("test")
time.sleep(1)
