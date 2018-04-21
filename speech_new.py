import speech_recognition as sr
import threading
from threading import Thread, current_thread
import time
from multiprocessing import Process, Queue, Manager 
import datetime
import sklearn.datasets
from sklearn.datasets import load_files
import sklearn.metrics
import sklearn.svm
import sklearn.naive_bayes
import numpy as np
from sklearn.naive_bayes import MultinomialNB
import sklearn.neighbors
from sklearn import svm
import sys, os, glob
from pprint import pprint

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
'''
import plac
import spacy
from spacy import displacy
import en_core_web_sm
'''
'''
import plac
import spacy
from spacy import displacy
import en_core_web_sm

def Allergies_Parse(phrase):
    # We just need to get allergen
    print("Nlp part for Allergies:")
    doc = nlp(phrase)
    allergen = 'allergen'

    allergen_flag = 1

    for count, token in enumerate(doc):
        # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
        if token.dep_ == 'pobj':
            allergen = token
            allergen_flag = 0

    if allergen_flag:
        for token in doc:
            if token.pos_ == 'NOUN' and token.dep_ == 'nsubj':
                allergen = token


    return str(allergen)




def Assessment_Parse(phrase):
    # Recognize terms for medical conditions / diagnoses.
    # Just find final assessment

    print("Nlp part for Assessment:")
    nlp = spacy.load('en')
    doc = nlp(phrase)
    condition = 'condition'
    condition_flag = 1

    for count, token in enumerate(doc):
        if token.dep_ == 'dobj':
            condition = token
            condition_flag = 0
        elif token.dep_ == 'pobj':
            condition = token
            condition_flag = 0

    if condition_flag:
        for token in doc:
            if token.pos_ == 'NOUN' and token.dep_ == 'nsubj':
                condition = token

    return str(condition)

def FamilyHistory_Parse(phrase):
    # We need to capture condtion and the family member


    print("Nlp part for Family History:")

    nlp = spacy.load('en')
    doc = nlp(phrase)


    # # This is used to see if there is a family member from our list

    condition = 'condition'
    fam_relation = 'family relation'

    fam_flag = 1
    for word in doc:
        if str(word) in FAMILY_LIST:
            fam_flag = 0
            fam_relation = word



    # Family members tend to be the subject noun of the sentence
    # The condition tends to be the direct object.
    for count, token in enumerate(doc):
        # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
        if token.dep_ == 'dobj':
            condition = token
        elif fam_flag == 1 and token.pos_ == 'NOUN' and token.dep_ == 'nsubj':
            fam_relation = token

    return str(condition), str(fam_relation)

def HPI_Parse(phrase):
    # Just get the conditions and symptoms from patient
    # Also capture the duration

    print("Nlp part for HPI:")

    doc = nlp(phrase)
    condition = 'condition'
    duration = 'duration'


    for count, token in enumerate(doc):
        # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
        if token.dep_ == 'dobj':
            condition = token
        if token.dep_ == 'pobj' and doc[count - 1].dep_ == 'prep':
            condition = token
        last_word = token

    for ent in doc.ents:
        # print(ent.text, ent.start_char, ent.end_char, ent.label_)
        if ent.label_ == 'DATE':
            duration = ent.label_

    if duration == 'duration' and condition == 'condition':
        return
    elif duration != 'duration' and condition == 'condition':
        return duration
    elif duration == 'duration' and condition != 'condition':
        return condition
    else:
        return str(condition), str(duration)


def MedicalHistory_Parse(phrase):
    # Recognize conditions and diagnoses from past


    print("Nlp part for Medical History:")

    doc = nlp(phrase)
    MedHis = 'Medical History'
    compound_flag = 0

    for count, token in enumerate(doc):
        if count >= 1:
            if doc[count -1].dep_ == 'compund' or doc[count -1].dep_ == 'nummound':
                word = str(doc[count -1]) + " " + str(token)
                compound_flag = 1
            else:
                compound_flag = 0

        if token.dep_ == 'dobj':
            MedHis = word if compound_flag == 1 else token
        if token.dep_ == 'pobj' and doc[count - 1].dep_ == 'prep':
            MedHis = word if compound_flag == 1 else token

    return str(MedHis)

def Medications_Parse(phrase):
    # Recognize medications patient is currently using
    # MIGHT BE A GOOD PLACE FOR A MEDICATIONS ARRAY

    print("Nlp part for Medications:")

    doc = nlp(phrase)
    Meds = 'Medication'
    compound_flag = 0

    for count, token in enumerate(doc):
        if count >= 1:
            if doc[count -1].dep_ == 'compund' or doc[count -1].dep_ == 'nummound':
                word = str(doc[count -1]) + " " + str(token)
                compound_flag = 1
            else:
                compound_flag = 0

        if token.dep_ == 'dobj':
            Meds = word if compound_flag == 1 else token
        if token.dep_ == 'pobj' and doc[count - 1].dep_ == 'prep':
            Meds = word if compound_flag == 1 else token

    return str(Meds)

def PatientInstructions_Parse(phrase):
    # Just pass whole sentence

    return str(phrase)

    pass
def PhysicalExam_Parse(phrase):
    # Recognize terms for conditions that can be identified during physical exam
    # GOOD PLACE TO PUT IN A LIST OF PHYSCIAL EXAMS
    keywords = []

    for chunk in (phrase.noun_chunks):
        if chunk.root.dep_ == 'dobj' or chunk.root.dep_ == 'pobj':
            keywords.append(chunk.text)

    return keywords


def Plan_Parse(phrase):
    # * Recognize lab tests and automate ordering.
    # * Recognize prescriptions and automate ordering.
    # * Record action items as sentences and ask if they should be added to the plan.


    print("Nlp part for Plan:")

    doc = nlp(phrase)
    PhysExam = 'Physical Exam'
    compound_flag = 0

    for count, token in enumerate(doc):
        if count >= 1:
            if doc[count -1].dep_ == 'compund' or doc[count -1].dep_ == 'nummound':
                word = str(doc[count -1]) + " " + str(token)
                compound_flag = 1
            else:
                compound_flag = 0

        if token.dep_ == 'dobj':
            PhysExam = word if compound_flag == 1 else token
        if token.dep_ == 'pobj' and doc[count - 1].dep_ == 'prep':
            PhysExam = word if compound_flag == 1 else token

    return str(PhysExam)


def ReviewOfSystems_Parse(phrase):
    # Recognize terms provided is ROS doc and synonyms
    # Make a list from the ROS document

    keywords = []

    for chunk in (phrase.noun_chunks):
        if chunk.root.dep_ == 'dobj' or chunk.root.dep_ == 'pobj':
            keywords.append(chunk.text)

    return keywords
'''
def Vote(text):
	VoteB,VoteD = HardClassify(text)
	VoteML = MLClassify(text)
	Advanced = 0 
	if (Advanced):
		return VoteML
	else:
		if VoteD == VoteB:
			return VoteB
		else:
			return VoteML



def HardClassify(text):
        # A simple example of the conversation
        # This information will be pass by the speech recognize API( text[i] = marker + r.recognize_google(audio[i]) )
        # Note: recognize result from Google Speech API does not include any punctuation
        """
            text = []
            text.append("")
            text[0] = "[D] Hello Mr Potter could you please talk something about yourself"
            text.append("")
            text[1] = "[P] Hello Dr Ingham I am Harry Potter a student 21 years old 170 centimeters height 65 kilograms weight Currently catched a cold"
            text.append("")
            text[2] = "[D] What are the symptoms that trouble you Specifically"
            text.append("")
            text[3] = "[P] I have been coughing for half a week and have been running a fever"
            text.append("")
            text[4] = "[D] I see and do you allergy to any kind of medicine"
            text.append("")
            text[5] = "[P] Might be Penicillins my former doctor told me don't use that"
            
            """
        # A sample keyword database
        # The actual database should be generated by SQL or a Spider
        keywordindex = ["Me", "You", "Information", "Time", "Billing", "Symptoms", "Allergy", "Family", "Organ","Be","Medicine","Instructions","Terms","Disease","Test"]
        keywordcategory = []
        keywordcategory.append("")
        #Me
        keywordcategory[0] = {"am","I'm"}
        keywordcategory.append("")
        #You
        keywordcategory[1] = {"You","you're","your"}
        keywordcategory.append("")
        #Information
        keywordcategory[2] = {"centimeter","centimeters","meter","meters","inch","inchs","worker", "student" , "teacher", "professor"}
        keywordcategory.append("")
        #Time
        keywordcategory[3] = {"days","day","weeks","week","year","years","month","months","recent","recently","current","time"}
        keywordcategory.append("")
        #Billing
        keywordcategory[4] = {"worker", "student" , "teacher", "professor"}
        keywordcategory.append("")
        #Symptoms
        keywordcategory[5] = {"cough", "coughed", "coughing", "fever", "ache", "itch","headache","temperature","worn"}
        keywordcategory.append("")
        #Allergy
        keywordcategory[6] = {"penicillins" , "aspirins","drug allergy"}
        keywordcategory.append("")
        #Family
        keywordcategory[7] = {"father" , "mother", "dad", "mom", "grandpa", "grandma", "son", "daugher", "sister", "brother", "cousin", "wife", "husband"}
        keywordcategory.append("")
        #Organ
        keywordcategory[8] = {"head","eye","eyes","nose","ear","ears","mouth","leg","legs","heart","arm","arms","lung","lungs","wrist","facial","face","arches","hand","nose","oral","vaginal"}
        keywordcategory.append("")
        #Be
        keywordcategory[9] = {"is","am","are","was","were","be"}
        keywordcategory.append("")

        #Medicine
        keywordcategory[10] = {"antibiotic","Ora","film","cardolor","calomist","catapres","jalyn","Jetrea","fish oil","citamin B","Tarka","Tcis","Temodar","Yervoy","YAZ","saizen","salacyn","vitamin","uceris","jetrea","wellbutrin"}
        keywordcategory.append("")

        #Instructions
        keywordcategory[11] = {"rest","work","smoking","medication","water","exercises","fruit","vegetables","surgery","hospital","food"," water","sleep","meat"}
        keywordcategory.append("")

        #Terms
        keywordcategory[12] = {"swollen","yellow","wisdom","fracture","palsy","fallen","broken","fluid","hip","obesity"}
        keywordcategory.append("")
        #Disease
        keywordcategory[13] = {"obesity","cancer","candidiasis","varicella","variola","acne","baldness","itch","Benign","migratory","glossitis","blackheads","infection","overactive" ,"thyroid","fever","retinopathy","diabetic"}
        keywordcategory.append("")
        #Test
        keywordcategory[14] = {"test","hida","scan","hiv","testing","hpv","a1c","bone","ct","cancer","screening","density","blood","pressure","bun","nonstress","x-ray","xray","genetic","ferritin","tile","table"}
        keywordcategory.append("")
        # Splitting the text, and make the text not sensitive to the upper/lower cases
        textsplit = []
        textsplit = text.split()
            #for i in range (0, len(text)):
            #text[i] = text[i].lower()
            #textsplit.append(text[i].split())
        #print (textsplit[i])
        
        # Analyzing the text (Keyword Comparing)
        record = []
        for k in range (0, len(keywordcategory)):
            record.append([])


        cateLookUp = {"Me":0,"You": 1, "Information": 2, "Time": 3, "Billing": 4, \
            "Symptoms": 5, "Allergy": 6, "Family": 7, "Organ": 8,"Be": 9,"Medicine": 10, \
            "Instructions": 11,"Terms": 12,"Disease":13,"Test":14}
        tag = []
        Detected = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for o in range(0,len(textsplit)):
            tag.append(0)

        for j in range (0, len(textsplit)):
            for k in range (0, len(keywordcategory)):
                if textsplit[j] in keywordcategory[k] :
                            Detected[k] = 1
                            tag[j] = k
                            record[k].append(textsplit[j])
                            #if k == 5 :
                                #print("symptom detected")
                                #record[k].append(textsplit[j])
                                #if k == 0 :
                                    #print("name detected")
                                    #record[k].append(textsplit[j+1])
                            #if k == 1 or k == 2:
                                #print("time detect")
                                #record[k].append(textsplit[j-1])

        #Decision Tree Network
        print("DT result:")
        VoteD = "Special_Sets"
        # Symptom layer, detect symptoms
        if (len(record[cateLookUp['Disease']]) > 0):
            # Family Layer, detect family members
            if (len(record[cateLookUp['Family']]) > 0):
                # Report Family history
                VoteD = 'Family_History'
                print('Report Family history')
                #print(record[cateLookUp['Family']][0] + " : " + record[cateLookUp['Symptoms']][0])
            if (len(record[cateLookUp['You']]) > 0):
                # Report Assessment
                VoteD = 'Assessment'
                print('Report Assessment')
            # Time Layer, detect Time information
            elif (len(record[cateLookUp['Time']]) > 0):
                # Long period
                if ("year" in record[cateLookUp['Time']] \
                    or "years" in record[cateLookUp['Time']]):
                    # Report Problem list
                    VoteD = 'Medical_History'
                    print('Report Medical History')
                    #print(record[cateLookUp['Symptoms']])
                else: 
                    # Report History of present illness
                    VoteD = 'HPI'
                    print('Report HPI')
                    #print(record[cateLookUp['Symptoms']][0] + " for " + record[cateLookUp['Time']][0])
            else: 
                # Report Medical History
                VoteD = 'Medical_History'
                print('Report Medical History')
                #print(record[cateLookUp['Symptoms']])

        elif (len(record[cateLookUp['Symptoms']]) > 0):
            if (len(record[cateLookUp['Time']]) > 0):
                VoteD = 'HPI'
                print('Report HPI')
        # No symptom found, detect organ
        elif (len(record[cateLookUp['Organ']]) > 0):
            if (len(record[cateLookUp['Terms']]) > 0):
            # Report phycial Exam
                VoteD = 'Physical_Exam'
                print('Report physical Exam')
                #print(text)
        # check allergy
        elif (len(record[cateLookUp['Allergy']]) > 0):
            VoteD = 'Allergy'
            print('Report allergy')

        elif (len(record[cateLookUp['Me']]) > 0):
            if (len(record[cateLookUp['Medicine']]) > 0):
                VoteD = 'Medications'
                print('Report Medications')

        elif (len(record[cateLookUp['You']]) > 0):
            if (len(record[cateLookUp['Instructions']]) > 0):
                VoteD = 'Instructions'
                print('Report Patient Instructions')
            elif (len(record[cateLookUp['Test']]) > 0):
                VoteD = 'Plan'
                print('Report Plan')
        else:
            VoteD = 'Special_Sets'
            print('Enter special sets')
                        #End the Conversation
            if (("all" in textsplit) and ("bye" in textsplit)):
                    print("Conversation End")
                    exit(0)

            if (("questions" in textsplit) and ("yes" in textsplit) and ("no" in textsplit)):
                    negatives_flag = 1








        #Naive Fixed Bayes


        #Currently four kinds of outputs enabled.


        cateLookUp = {"Me":0,"You": 1, "Information": 2, "Time": 3, "Billing": 4,"Symptoms": 5, "Allergy": 6, "Family": 7, "Organ": 8,"Be": 9,"Medicine": 10,"Instructions":11,"Terms": 12,"Disease":13,"Test":14}
        ResultLookUp = ["Allergy","Assessment","Family_History","HPI",\
                        "Medcial_History","Medications","Instructions",\
                        "Physical_Exam","Plan","Review"]
        ResultProbB = [1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]
#                        0   1   2   3   4   5   6   7   8   9   10  11  12  13  14
        BayesTable = [ [0.5,0.1,0.1,0.1,0.1,0.2,0.9,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.3], \
                       [0.1,0.5,0.1,0.1,0.1,0.5,0.3,0.1,0.1,0.1,0.1,0.1,0.1,0.8,0.4], \
                       [0.3,0.1,0.1,0.1,0.1,0.5,0.1,0.8,0.1,0.1,0.1,0.1,0.1,0.8,0.2], \
                       [0.7,0.1,0.1,0.6,0.1,0.9,0.1,0.1,0.5,0.1,0.1,0.1,0.1,0.8,0.3], \
                       [0.7,0.1,0.1,0.8,0.1,0.6,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.9,0.3], \
                       [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1], \
                       [0.4,0.7,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.8,0.7,0.1,0.1,0.4], \
                       [0.5,0.6,0.1,0.1,0.1,0.6,0.1,0.1,0.7,0.1,0.1,0.1,0.8,0.5,0.1], \
                       [0.4,0.6,0.1,0.1,0.1,0.4,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.5,0.8], \
                       [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1], \
                      ]




        for i in range(0,len(ResultProbB)) :
            for j in range(0,len(BayesTable[i])) :
                if Detected[j] == 1:
                    ResultProbB[i] = ResultProbB[i] * BayesTable[i][j]
                else:
                    ResultProbB[i] = ResultProbB[i] * 0.5
        ##print("The result of Bayes Table:")
        largest = 0
        largestindex = 0
        for i in range(0,len(ResultProbB)) :
         ##   print(ResultProbB[i])
            if ResultProbB[i] > largest:
                largest = ResultProbB[i]
                largestindex = i
        print("NB result",ResultLookUp[largestindex])

        VoteB = ResultLookUp[largestindex]
        #print("vote result")
        #print(VoteB,VoteD)
        return VoteB,VoteD
'''
        if VoteB == VoteD :
            print("Quite sure about the classify result, generating training data")
            currenttime = datetime.datetime.now()
            currenttime = ''.join(["Date:",str(currenttime)])
            filename = ''.join([currenttime,".txt"])
            fullfilename = ''.join([VoteB,"/",filename])
            trainingfile = open(fullfilename,"w")
            trainingfile.write(text)
            trainingfile.close
'''
            #Output the extracting results
        #for i in range (0, len(keywordcategory)):
            #print (keywordindex[i])
            #print (record[i])





def MLClassify(text):

	'''
	test_path = './testing'
	test_files = sklearn.datasets.load_files(test_path, encoding = 'latin1', load_content=True)
	#
	# print(test_files)
	print("test_files")
	print(test_files.data)
	X_test_counts = count_vect.transform(test_files.data)
	print("X_test_counts")
	print(X_test_counts.toarray())
	X_test_tfidf = tfidf_transformer.transform(X_test_counts)
	print("X_test_tfidf")
	print(X_test_tfidf.toarray())
	# print(X_test_counts.shape)
	predicted = svm.predict_proba(X_test_counts)
	#
	print("svm.predict")
	print(svm.predict(X_test_counts))
	print("predicted")
	print(predicted)
	'''

	#count_vect = CountVectorizer()
	#print("train",files)
	X_test_countst = count_vect.transform([text])

	X_test_tfidft = tfidf_transformer.transform(X_test_countst)
	predict_result = svmi.predict_proba(X_test_tfidft)
	#print("test = " , svmi.predict_proba(X_test_tfidft))
	#print(predict_result.shape)
	#print(predict_result[0][1])
	#print(predict_result.shape[1])
	#print(svmi.predict(X_test_countst))
	#print(X_test_countst.toarray())
	MLcategory = ["Allergies","Assessment","Family_History","HPI","Medical_History","Medications","Patient_Instructions","Physical_Exam","Plan","Review_of_Systems"]
	print("ML result:",MLcategory[svmi.predict(X_test_countst)[0]])
        '''
    	if category == 'Allergies' :
        	allergen = Allergies_Parse(phrase)
        	print("allergic to: " + allergen)

    	elif category == 'Assessment':
        	print("Go to Assessment")
        	print(Assessment_Parse(phrase))

    	elif category == 'Family_History':
        	print("Go to FamilyHistory")
        	print(FamilyHistory_Parse(phrase))

    	elif category == 'HPI':
        	print("Go to HPI")
        	print(HPI_Parse(phrase))

    	elif category == 'Medical_History':
        	print("Go to MedicalHistory")
        	print(MedicalHistory_Parse(phrase))

    	elif category == 'Medications':
        	print("Go to Medications")
        	print(Medications_Parse(phrase))

    	elif category == 'Patient_Instructions':
        	print("Go to PatientInstructions")
        	print(PatientInstructions_Parse(phrase))

    	elif category == 'Physical_Exam':
        	print("Go to PhysicalExam")
        	print(PhysicalExam_Parse(phrase))

    	elif category == 'Plan':
        	print("Go to Plan")
        	print(Plan_Parse(phrase))

    	elif category == 'Review_of_Systems':
        	print("Go to ReviewOfSystems")
        	print(ReviewOfSystems_Parse(phrase))

    	else:
        	print("No category")
        '''
	return MLcategory[svmi.predict(X_test_countst)[0]]

	#for i in range(predict_result.shape[1]):
def Record(person):
	#target the microphone by id or by name
	if (person == "doctor"):
		#mic_name = "USB PnP Sound Device" 
		device_id = 0
	else:
		mic_name = "R555"
		device_id = 2
    	#mic_name = "USB PnP Sound Device"
    #Sample rate is how often values are recorded
	sample_rate = 48000
    #Chunk is like a buffer, stores 2048 samples (bytes of data)
    #Advisable to use powers of 2 such as 1024 or 2048
	chunk_size = 2048

    #generate a list of all audio cards/microphones
	mic_list = sr.Microphone.list_microphone_names()
	print mic_list
	# for i, microphone_name in enumerate(mic_list):
	# 	if microphone_name == mic_name:
	# 		device_id = i

    #use the microphone as source for input. Here, we also specify
    #which device ID to specifically look for incase the microphone
    #is not working, an error will pop up saying "device_id undefined"
	with sr.Microphone(device_index = device_id, sample_rate = sample_rate, chunk_size = chunk_size) as source:
		recog.adjust_for_ambient_noise(source)
		recog.pause_threshold = 0.7
		while 1:
            #listens for the user's input
			audio = recog.listen(source)
			t_recog = threading.Thread(target = Recogize, name = person, args = (audio,))
			t_recog.start()

def Recogize(audio):
	person = current_thread().getName()
	try:
		index = queue_index.get()
		queue_index.put(index+1)
		text = recog.recognize_google(audio)
		# to prevent strange "u'somestring'" in print
		text = text.encode("utf8")
		queue_sentence.put({index: person + ": " + text})
	#error occurs when google could not understand what was said     
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")    
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))

# OutputSingle(): convert one dialoge sentence dictionary to string, and feed 
# into text classify function.
def OutputSingle():
	pick = queue_sentence.get()
	# add to whole dictionary
	log.update(pick)
	# send a string to text classification
	index = pick.keys()[0]
	output = str(index)+ " " + pick[index]
	classify_result = Vote(output)
	print output
	print ("Vote result:",classify_result)
    	ResultLookUp = ["Allergies","Assessment","Family_History","HPI","Medical_History","Medications","Patient_Instructions","Physical_Exam","Plan","Review_of_Systems"]
    	#file = ['','','','','','','','','','']
    	#contents = ['','','','','','','','','','']
        newline = output + "," +classify_result +"\n"
        f = open("./data/text.txt","a")
        f.write(newline)
        print("Writting:  ", newline)
        f.close()
        '''
    	for i in range(0,10):
        	#print (i)
        	if ResultLookUp[i] == classify_result:
            		file[i] = "./pipetest/" + ResultLookUp[i] + ".txt"
            		f = open(file[i],"w")
            		f.write(output)
            		print("Writting  ",output,"  To  ",ResultLookUp[i])
            		f.close()
                    '''
	# check for end of visit
	if "quit" in pick.values()[0]:
		p_doctor.terminate()
		p_patient.terminate()
		return 1
	return 0

# OutputWhole(log): sort the orderless dialoge dictionary, produce ordered 
# dialoge list
# @param[in] log: a dictionary containning all the sentences
def OutputWhole(log):
	temp = log
	whole = []
	for i in sorted(log.keys()):
		whole.append(temp[i])
	return whole

if __name__ == '__main__':
	log = {}
	recog = sr.Recognizer()
	queue_sentence = Manager().Queue()
	queue_index = Queue()
	queue_index.put(1)
	# pre-train the bayes network 
	# 
	# 
	#
	# 
        '''
    	nlp = en_core_web_sm.load()

    	FAMILY_LIST = ['father', 'mother', 'parent', 'mom', 'dad', 'son', 'daugther',
               'sister', 'brother', 'uncle', 'aunt', 'grandpa', 'grandma', 'grandfather',
               'grandmother', 'grandparents', 'cousin', 'neice', 'uncle', 'aunt'
                ]
        '''
	path = './dataset'
	files = sklearn.datasets.load_files(path, encoding = 'latin1', decode_error = 'replace', load_content=True, random_state=3)
	# print(files)
	count_vect = CountVectorizer()

	X_train_counts = count_vect.fit_transform(files.data)

	tfidf_transformer = TfidfTransformer()
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
	# print(X_train_tfidf)
	# print("Target")
	# print(files)
	# print()
	# print((X_train_counts))
	svmi = svm.SVC(kernel = 'linear', probability=True)
	X = X_train_tfidf
	# pprint(files.values())
	Y = files["target"]
	print("Shapes")
	print(X.shape)
	print(Y.shape)
	h = svmi.fit(X, Y)
	print(h)
	# print("Now doing test files")
	#
	#
	#
	#
	p_doctor = Process(target = Record, args=("doctor",))
	p_patient = Process(target = Record, args=("patient",))
	p_patient.start()
	p_doctor.start()
	quit_flag = 0
	while(not quit_flag):
		quit_flag = OutputSingle()
	print OutputWhole(log)
