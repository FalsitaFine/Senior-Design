#Python 2.x program for Speech Recognition

import speech_recognition as sr
import threading
import time


def startRecording(type):
    
    #enter the name of usb microphone that you found
    #using lsusb
    #the following name is only used as an example
    mic_name = "USB PnP Sound Device"
    mic_name_2 = "Built-in Microphone"
    #Sample rate is how often values are recorded
    sample_rate = 48000
    #Chunk is like a buffer. It stores 2048 samples (bytes of data)
    #here.
    #it is advisable to use powers of 2 such as 1024 or 2048
    chunk_size = 2048
    #Initialize the recognizer
    r = sr.Recognizer()
    r2 = sr.Recognizer()


    #generate a list of all audio cards/microphones
    mic_list = sr.Microphone.list_microphone_names()


    #the following loop aims to set the device ID of the mic that
    #we specifically want to use to avoid ambiguity.
    for i, microphone_name in enumerate(mic_list):
        if microphone_name == mic_name:
            device_id = i
                print(device_id)
    for i, microphone_name in enumerate(mic_list):
        if microphone_name == mic_name_2:
            device_id_2 = i
            print(device_id_2)

    audio = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    text = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #use the microphone as source for input. Here, we also specify
    #which device ID to specifically look for incase the microphone
    #is not working, an error will pop up saying "device_id undefined"

    k = 0
    wholetext = ""
    while k<20:
        k = k + 1
        if(type == "patient"):
            with sr.Microphone(device_index = device_id_2, sample_rate = sample_rate, chunk_size = chunk_size) as source:
                #wait for a second to let the recognizer adjust the
                #energy threshold based on the surrounding noise level
                r.adjust_for_ambient_noise(source)
                r.pause_threshold = 2.0
                print(source)
                
                print "Patient, Please Say Something(with USB microphone)"
                #listens for the user's input
                audio[2*k-1] = r.listen(source)
                print "Record finish, processing"
                Process_Read_1 = threading.Thread(target = Rec_Part_1, name = "test_1", args = (audio[2*k-1],))
                Process_Read_1.start()
                print(threading.enumerate())

        if(type == "doctor"):
        with sr.Microphone(device_index = device_id_2, sample_rate = sample_rate, chunk_size = chunk_size) as source_2:
            #wait for a second to let the recognizer adjust the
            #energy threshold based on the surrounding noise level
            r2.adjust_for_ambient_noise(source_2)
            r2.pause_threshold = 2.0
            print(source_2)
            
            print "Doctor, Please Say Something"
            #listens for the user's input
            audio[2*k] = r2.listen(source_2)
            print "Record finish, processing"
            Process_Read_2 = threading.Thread(target = Rec_Part_2, name = "test_doctor", args = (audio[2*k],))
            Process_Read_2.start()
            print(threading.enumerate())




def Rec_Part_2(audio):
    try:
        text[2*k] = r2.recognize_google(audio)
        print "doctor said: " + text[2*k]
        #wholetext = wholetext + text[2*k]
        Process(text[2*k])
        
        #error occurs when google could not understand what was said
        
    except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        
    except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

def Rec_Part_1(audio):
    try:
        text[2*k-1] = r.recognize_google(audio)
        print "patient said: " + text[2*k-1]
        #wholetext = wholetext + text[2*k-1]
        Process(text[2*k-1])
            
            #error occurs when google could not understand what was said
            
    except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            
    except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

def Process(text):
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
        keywordindex = ["Name", "Height", "Weight", "Billing", "Symptoms", "Allergy"]
        keywordcategory = []
        keywordcategory.append("")
        keywordcategory[0] = {"am","I'm"}
        keywordcategory.append("")
        keywordcategory[1] = {"centimeter","centimeters","meter","meters","inch","inchs"}
        keywordcategory.append("")
        keywordcategory[2] = {"kilograms"}
        keywordcategory.append("")
        keywordcategory[3] = {"worker", "student" , "teacher", "professor"}
        keywordcategory.append("")
        keywordcategory[4] = {"cough", "coughed", "coughing", "fever", "ache", "itch"}
        keywordcategory.append("")
        keywordcategory[5] = {"penicillins" , "aspirins"}
        
        # Splitting the text, and make the text not sensitive to the upper/lower cases
        textsplit = []
        print(text)
        textsplit = text.split()
            #for i in range (0, len(text)):
            #text[i] = text[i].lower()
            #textsplit.append(text[i].split())
        #print (textsplit[i])
        
        # Analyzing the text (Keyword Comparing)
        record = []
        for k in range (0, len(keywordcategory)):
            record.append([])


#for i in range (0, len(textsplit)):
#           for j in range (0, len(textsplit[i])):
        for j in range (0, len(textsplit)):
                for k in range (0, len(keywordcategory)):
                    if textsplit[j] in keywordcategory[k] :
                        if k >= 3 :
                            print("symptom detected")
                            record[k].append(textsplit[j])
                            if k == 0 :
                                record[k].append(textsplit[j+1])
                        if k == 1 or k == 2:
                            record[k].append(textsplit[j-1])


        #Output the extracting results


        for i in range (0, len(keywordcategory)):
            print (keywordindex[i])
            print (record[i])
        return 1



#enter the name of usb microphone that you found
#using lsusb
#the following name is only used as an example
mic_name = "USB PnP Sound Device"
mic_name_2 = "Built-in Microphone"
#Sample rate is how often values are recorded
sample_rate = 48000
#Chunk is like a buffer. It stores 2048 samples (bytes of data)
#here. 
#it is advisable to use powers of 2 such as 1024 or 2048
chunk_size = 2048
#Initialize the recognizer
r = sr.Recognizer()
r2 = sr.Recognizer()


#generate a list of all audio cards/microphones
mic_list = sr.Microphone.list_microphone_names()


#the following loop aims to set the device ID of the mic that
#we specifically want to use to avoid ambiguity.
for i, microphone_name in enumerate(mic_list):
	if microphone_name == mic_name:
		device_id = i
                print(device_id)
for i, microphone_name in enumerate(mic_list):
    if microphone_name == mic_name_2:
        device_id_2 = i
        print(device_id_2)

audio = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
text = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#use the microphone as source for input. Here, we also specify 
#which device ID to specifically look for incase the microphone 
#is not working, an error will pop up saying "device_id undefined"

k = 0
wholetext = ""
while k<20:
    k = k + 1

    with sr.Microphone(device_index = device_id_2, sample_rate = sample_rate, chunk_size = chunk_size) as source:
        #wait for a second to let the recognizer adjust the
        #energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2.0
        print(source)

        print "Patient, Please Say Something(with USB microphone)"
                        #listens for the user's input
        audio[2*k-1] = r.listen(source)
        print "Record finish, processing"
        Process_Read_1 = threading.Thread(target = Rec_Part_1, name = "test_1", args = (audio[2*k-1],))
        Process_Read_1.start()
        print(threading.enumerate())


    with sr.Microphone(device_index = device_id_2, sample_rate = sample_rate, chunk_size = chunk_size) as source_2:
        #wait for a second to let the recognizer adjust the
        #energy threshold based on the surrounding noise level
        r2.adjust_for_ambient_noise(source_2)
        r2.pause_threshold = 2.0
        print(source_2)

        print "Doctor, Please Say Something"
             #listens for the user's input
        audio[2*k] = r2.listen(source_2)
        print "Record finish, processing"
        Process_Read_2 = threading.Thread(target = Rec_Part_2, name = "test_doctor", args = (audio[2*k],))
        Process_Read_2.start()
        print(threading.enumerate())

 
