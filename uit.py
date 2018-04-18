import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class EMRWindow(Gtk.Window):
	def __init__(self):
		K = 0 
		Gtk.Window.__init__(self, title="Electronic Medical Record")
#
		self.set_default_size(800,600)
		grid = Gtk.Grid()
		self.add(grid)
		name = Gtk.Label()
		name.set_markup("Arietta.Fine")
		age = Gtk.Label()
		age.set_text("17 years old")
		gender = Gtk.Label()
		gender.set_text("Female")
		box = Gtk.Box(spacing=10)
		box.pack_start(name, False, False, 10)
		box.pack_start(age, False, False, 10)
		box.pack_start(gender, False, False, 10)
		grid.attach(box,0,0,4,1)
		color = Gdk.color_parse("gray")
		rgba = Gdk.RGBA.from_color(color)
        # Medications
		self.meds_store = Gtk.ListStore(str)
		self.meds_store.append(["Advil"])
		#self.meds_store.append(["Antibiotics"])
		#self.meds_store.append(["Benedryl"])
		self.meds_store[0] = [text[5]]
		meds = Gtk.TreeView(self.meds_store)
		meds_renderer = Gtk.CellRendererText()
		meds_renderer.set_property("editable", True)
		meds_renderer.connect("edited", self.text_edited,self.meds_store)
		column = Gtk.TreeViewColumn("Medications", meds_renderer, text=0)
		meds.append_column(column)
		select = meds.get_selection()
		select.connect("changed", self.on_tree_selection_changed)
		grid.attach(meds, 0, 1, 1, 3)
		#self.meds_store[1] = ["TTTT"]


		# Allergies
		self.allergies_store = Gtk.ListStore(str)
		#allergies_store.append(["Penicillin"])
		self.allergies_store.append(["empty"])
		self.allergies_store[0] = [text[0]]
		print("refreshed",text[1])

		allergies = Gtk.TreeView(self.allergies_store)
		allergy_renderer = Gtk.CellRendererText()
		allergy_renderer.set_property("editable", True)
		allergy_renderer.connect("edited", self.text_edited, self.allergies_store)
		column = Gtk.TreeViewColumn("Allergies", allergy_renderer, text=0)
		allergies.append_column(column)
		select = allergies.get_selection()
		select.connect("changed", self.on_tree_selection_changed)
		grid.attach(allergies, 1, 1, 1, 3)
#		allergies.override_background_color(Gtk.StateFlags.NORMAL,rgba);
        
        # Family History
		self.familyHistory_store = Gtk.ListStore(str)
		#familyHistory_store.append(["Father - heart condition"])
		#familyHistory_store.append(["Mother - diabetes"])
		self.familyHistory_store.append([text[2]])
		familyHistory = Gtk.TreeView(self.familyHistory_store)
		fh_renderer = Gtk.CellRendererText()
		fh_renderer.set_property("editable", True)
		fh_renderer.connect("edited", self.text_edited, self.familyHistory_store)
		column = Gtk.TreeViewColumn("Family History", fh_renderer, text=0)
		familyHistory.append_column(column)
		select = familyHistory.get_selection()
		select.connect("changed", self.on_tree_selection_changed)
		grid.attach(familyHistory, 2, 1, 1, 3)




		# Medical History
		self.medicalHistory_store = Gtk.ListStore(str)
		self.medicalHistory_store.append([text[4]])
		#medicalHistory_store.append(["Past Medical Conditions"])
		medicalHistory = Gtk.TreeView(self.medicalHistory_store)
		mh_renderer = Gtk.CellRendererText()
		mh_renderer.set_property("editable", True)
		mh_renderer.connect("edited", self.text_edited,self.medicalHistory_store)
		column = Gtk.TreeViewColumn("Medical History", mh_renderer, text=0)
		medicalHistory.append_column(column)
		select = medicalHistory.get_selection()
		select.connect("changed", self.on_tree_selection_changed)
		grid.attach(medicalHistory,3,1,1,3)
		
		# History of Present Illness (HPI)
		hpiLabel = Gtk.Label()
		hpiLabel.set_text("History of Present Illness (HPI)")
		hpiView = Gtk.TextView()
		hpiView.set_wrap_mode(Gtk.WrapMode.WORD)
		self.hpiBuffer = hpiView.get_buffer()
		self.hpiBuffer.set_text(text[3])
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		vbox.pack_start(hpiLabel,True,True,0)
		vbox.pack_start(hpiView,True,True,0)
		grid.attach(vbox,0,5,2,4)
		
		# Review of Systems (ROS)
		rosLabel = Gtk.Label()
		rosLabel.set_text("Reviw of Systems (ROS)")
		rosView = Gtk.TextView()
		rosView.set_wrap_mode(Gtk.WrapMode.WORD)
		self.rosBuffer = rosView.get_buffer()
		self.rosBuffer.set_text(text[9])
		rosBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		rosBox.pack_start(rosLabel,False,False,0)
		rosBox.pack_start(rosView,False,False,0)
		grid.attach(rosBox,2,5,2,4)
		
		# Physical Exam
		peLabel = Gtk.Label()
		peLabel.set_text("Physical Exam")
		peView = Gtk.TextView()
		peView.set_wrap_mode(Gtk.WrapMode.WORD)
		self.peBuffer = peView.get_buffer()
		self.peBuffer.set_text(text[7])
		peBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		peBox.pack_start(peLabel,False,False,0)
		peBox.pack_start(peView,False,False,0)
		grid.attach(peBox,0,9,2,4)
		
		# Assessment
		aLabel = Gtk.Label()
		aLabel.set_text("Assessment")
		aView = Gtk.TextView()
		aView.set_wrap_mode(Gtk.WrapMode.WORD)
		self.aBuffer = aView.get_buffer()
		self.aBuffer.set_text(text[1])
		aBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		aBox.pack_start(aLabel,False,False,0)
		aBox.pack_start(aView,False,False,0)
		grid.attach(aBox,2,9,2,4)
		
		# Plan
		planLabel = Gtk.Label()
		planLabel.set_text("Plan")
		planView = Gtk.TextView()
		planView.set_wrap_mode(Gtk.WrapMode.WORD)
		self.planBuffer = planView.get_buffer()
		self.planBuffer.set_text(text[8])
		planBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		planBox.pack_start(planLabel,False,False,0)
		planBox.pack_start(planView,False,False,0)
		grid.attach(planBox,0,13,2,4)
		
		# Patient Instructions
		piLabel = Gtk.Label()
		piLabel.set_text("Patient Instructions")
		piView = Gtk.TextView()
		piView.set_wrap_mode(Gtk.WrapMode.WORD)
		self.piBuffer = piView.get_buffer()
		self.piBuffer.set_text(text[6])
		piBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		piBox.pack_start(piLabel,False,False,0)
		piBox.pack_start(piView,False,False,0)
		grid.attach(piBox,2,13,2,4)

		#Buttons
		button = Gtk.Button.new_with_label("Save")
		button.connect("clicked", self.saveEMR)
		box.pack_start(button, True, True, 0)

		button = Gtk.Button.new_with_label("Refresh")
		button.connect("clicked", self.refresh)
		box.pack_start(button, True, True, 0)

		button = Gtk.Button.new_with_label("Generate")
		button.connect("clicked", self.generateEMR)
		box.pack_start(button, True, True, 0)


		
	def text_edited(self, widget, path, text, liststore):
		liststore[path][0] = text

	def generateEMR(self, button):
			ResultLookUp = ["Allergies","Assessment","Family_History","HPI","Medical_History","Medications","Patient_Instructions","Physical_Exam","Plan","Review_of_Systems"]
			start = self.aBuffer.get_start_iter()
			end = self.aBuffer.get_end_iter()
			Atext = self.aBuffer.get_text(start,end,True)
			start = self.hpiBuffer.get_start_iter()
			end = self.hpiBuffer.get_end_iter()
			HPItext = self.hpiBuffer.get_text(start,end,True)
			start = self.piBuffer.get_start_iter()
			end = self.piBuffer.get_end_iter()
			PItext = self.piBuffer.get_text(start,end,True)
			start = self.planBuffer.get_start_iter()
			end = self.planBuffer.get_end_iter()
			plantext = self.planBuffer.get_text(start,end,True)
			start = self.rosBuffer.get_start_iter()
			end = self.rosBuffer.get_end_iter()
			rostext = self.rosBuffer.get_text(start,end,True)
			start = self.peBuffer.get_start_iter()
			end = self.peBuffer.get_end_iter()
			petext = self.peBuffer.get_text(start,end,True)
			
			html = "<!DOCTYPE html><html><head><meta charset = \"utf-8\"><title>EMR Table</title><link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\"></head><h2>EMR Table</h2><br><br><br><div id =\"Etable\"><table id = \"EMRTable\"><caption>Electrical Medical Record</caption><tr><th>Category</th><th>Content</th></tr>"

			htmlw = "./EMRresult.html"
			f = open(htmlw,'w')


			file = ['','','','','','','','','','']
			contents = ['','','','','','','','','','']
			for i in range(0,10):
				html = html + "<tr><th>" + ResultLookUp[i]+ "</th><th>"
				print (i)
				if (i == 0):
					html = html + self.allergies_store[0][0]
				elif (i == 1):
					html = html + Atext
				elif (i == 2):
					html = html + self.familyHistory_store[0][0]
				elif (i == 3):
					html = html + HPItext
				elif (i == 4):
					html = html + self.medicalHistory_store[0][0]
				elif (i == 5):
					html = html + self.meds_store[0][0]
				elif (i == 6):
					html = html + PItext
				elif (i == 7):
					html = html + petext
				elif (i == 8):
					html = html +plantext
				elif (i == 9):
					html = html +rostext
				html = html + "</th></tr>"
			html = html + "</table></div></body></html>"
			f.write(html)
			f.close()
		
	def on_tree_selection_changed(self,selection):
		model, treeiter = selection.get_selected()
		if treeiter is not None:
			print("You selected", model[treeiter][0]) 
	def refresh(self,button):
			text[1] = "changed text"
			self.meds_store[0] = ["test"]
			print(self.meds_store[0][0])
			catelookup = ["Family_History", "Allergies","Physical_Exam","HPI"]
			file = ['','','','']
			contents = ['','','','']
			for i in range(0,3):
				print (i)
				file[i] = "./pipe/" + catelookup[i] + ".txt"
				f = open(file[i])
				contents[i] = f.read()
				print(contents[i])
				f.close()

	def saveEMR(self,button):
			ResultLookUp = ["Allergies","Assessment","Family_History","HPI","Medical_History","Medications","Patient_Instructions","Physical_Exam","Plan","Review_of_Systems"]
			start = self.aBuffer.get_start_iter()
			end = self.aBuffer.get_end_iter()
			Atext = self.aBuffer.get_text(start,end,True)
			start = self.hpiBuffer.get_start_iter()
			end = self.hpiBuffer.get_end_iter()
			HPItext = self.hpiBuffer.get_text(start,end,True)
			start = self.piBuffer.get_start_iter()
			end = self.piBuffer.get_end_iter()
			PItext = self.piBuffer.get_text(start,end,True)
			start = self.planBuffer.get_start_iter()
			end = self.planBuffer.get_end_iter()
			plantext = self.planBuffer.get_text(start,end,True)
			start = self.rosBuffer.get_start_iter()
			end = self.rosBuffer.get_end_iter()
			rostext = self.rosBuffer.get_text(start,end,True)
			start = self.peBuffer.get_start_iter()
			end = self.peBuffer.get_end_iter()
			petext = self.peBuffer.get_text(start,end,True)
			
			
			file = ['','','','','','','','','','']
			contents = ['','','','','','','','','','']
			for i in range(0,10):
				print (i)
				file[i] = "./result/" + ResultLookUp[i] + ".txt"
				f = open(file[i],'w')
				if (i == 0):
					f.write(self.allergies_store[0][0])
				elif (i == 1):
					f.write(Atext)
				elif (i == 2):
					f.write(self.familyHistory_store[0][0])
				elif (i == 3):
					f.write(HPItext)
				elif (i == 4):
					f.write(self.medicalHistory_store[0][0])
				elif (i == 5):
					f.write(self.meds_store[0][0])
				elif (i == 6):
					f.write(PItext)
				elif (i == 7):
					f.write(petext)
				elif (i == 8):
					f.write(plantext)
				elif (i == 9):
					f.write(rostext)
				print(contents[i])
				f.close()





	
def readpipe(path):
	#catelookup = ["Family_History", "Allergies","Physical_Exam","HPI"]
	ResultLookUp = ["Allergies","Assessment","Family_History","HPI","Medical_History","Medications","Patient_Instructions","Physical_Exam","Plan","Review_of_Systems"]
	file = ['','','','','','','','','','']
	contents = ['','','','','','','','','','']
	for i in range(0,10):
		print (i)
		file[i] = "./pipe/" + ResultLookUp[i] + ".txt"
		f = open(file[i])
		contents[i] = f.read()
		print(contents[i])
		f.close()
	return contents

def saveresult(path):
	return 1

global text
text = readpipe("./pipe/")       
win = EMRWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()