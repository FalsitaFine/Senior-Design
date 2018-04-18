#coding:utf-8  
from Tkinter import *  
from ScrolledText import ScrolledText #文本滚动条  
import threading  
import time  
from PIL import ImageTk,Image  
from multiprocessing import Process, Queue, Manager 
  
  
  
def count(i):  
     for k in range(1, 100+1):  
        text.insert(END,'第'+str(i)+'线程count:  '+str(k)+'\n')  
        time.sleep(0.1)  
            
  
def fun():  
    for i in range(1, 5+1):  
        th=threading.Thread(target=count,args=(i,))  
        th.setDaemon(True) 
        th.start()  
    var.set('MDZZ')  
  
def test():
	th= threading.Thread(target = fun)  
	th.start()
  
root=Tk()  
root.title('九日王朝') 
root.geometry('+600+100')
image2 =Image.open(r'capture.png')  
background_image = ImageTk.PhotoImage(image2)  
textlabel=Label(root,image=background_image)  
textlabel.grid()  
text=ScrolledText(root,font=('微软雅黑',10),fg='blue')  
text.grid()  
button=Button(root,text='屠龙宝刀 点击就送',font=('微软雅黑',10),command=test)  
button.grid()  
var=StringVar()#设置变量  
label=Label(root,font=('微软雅黑',10),fg='red',textvariable=var)  
label.grid()  
var.set('我不断的洗澡，油腻的师姐在哪里')  
root.mainloop()  