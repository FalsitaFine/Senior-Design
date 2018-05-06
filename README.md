# Senior-Design: Automate EMR population

EE4951W Spring 2018, Senior Design group 10, UMN CSE

This contribution includes the Second Demo Version(The final version from us)

<li><a href="#Installation">Installation</a></li>

<li><a href="#Usage">Usage</a></li>

<li><a href="#Significant designs">Significant designs</a></li>

<li><a href="#Functions">List of Functions</a></li>


<a name="Installation">## Installation</a>:
This project needs a lot of pre-installation:
Python 2.7:

Spacy: for natural language process
https://spacy.io/

Sklearn,plac: for machine learning classification
http://scikit-learn.org/stable/

Tkinter: for User interface, this should come with python
https://docs.python.org/2/library/tkinter.html

Speech_recognition:
https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst

##<a name="Usage">Usage</a>:
1.First you need to modify the microphone id in *AutoEMR.py*: you can use build-in microphone, bluetooth microphone, or use USB to plug in a microphone. After connecting them in to your PC, run ```python AutoEMR.py``` at the project root directory, a list of microphones inputs and outputs will be print on the screen. Those names would come in pairs, the first one is input source and the second is the output source. Replace **device_id** in **linexxx** and **linexxx** of *AutoEMR.py* with the input source ids you want.

2.Open two terminal from the root directory, then enter these two instruction separately:
```
python AutoEMR.py
```
```
python AutoEMRUI.py
```
The order of opening two program doesn’t matter. The reason for running them in separate terminals is: some methods in Tkinter(UI) conflict with speech recognition API(Main program).

Now you can talk through two microphones and do the conversation!

We also provided the “MLtesting.py” file, which can be used as a tool for testing the training result of the machine learning program(during our development, we found that it is not convenient to testing the classifier by talking, this program can help you simply typing some sentences into the classifier and check its output).

##<a name="Significant designs">Significant designs</a>:
1.Parallel programing in Speech recognition:
Google speech recognition runs very slow and will block the whole program when we do serial programing, so we use worker threads to do the recognitions(in **line 317** of file *AutoEMR.py*). We use two process to record from two microphones(in **line 416,417** of file *AutoEMR.py*). The reason for not using thread here is that we get segmentation fault when replacing the process with thread. **Thread** and **Process** communicate through **Queue**. To learn more, please read https://docs.python.org/2/library/multiprocessing.html.

2.Machine learning algorithms:
We use SVM(Support Vector Machine) here. Naive Bayes Model can also be a solution, but for limited training data, SVM works significantly better.

3.Asynchronous UI:
Because Tkinter cannot support parallel programming well, we wrote a separate UI. Which will check a text file(modified by the main process) every second to communicate with the main process.

##<a name="Functions">List of Functions</a>:
###*AutoEMRUI.py*: User Interface and keywords capture are done


**KeywordsParse(parse,category)**: Capture keywords in a classified sentence. Only implemented for ‘allergy’, ‘family history’ and ‘medication’.

####**Gui**: Class for the graphic user interface.
**DrawBox(self,category,textin)**: Draw a text box or a list box on the main UI according to the UI configuration. This is used in the initialization of UI and refreshment when new information added.

**__init__(self, master, queue, initial, endCommand)**: initialization function of GUI class, generate the default window(with no information), create objects in the class.

**createDialog(self, keywords, category)**: Create a dialog box to the user when a new classification result is ready. The keywords displayed in textbox; category displayed in scroll bar so that user can modify; cancel button for user to ignore the message; accept button for the doctor add new information; merge button for add continued information.

**addInformation(self,info,category,dialog)**: Add the confirmed information to the main UI in a new line. Using **DrawBox** to refresh contents.

**MergeInformation(self,info,category,dialog)**: Add the confirmed information to the main UI but in the same line as previous message. Using **DrawBox** to refresh contents.
**generate(self)**: Generates a html EMR table, and write new training data in */trainingdata/*

**processIncoming(self)**: Read from *./data/text.txt* to check if there are new coming classification result. If exist, create new dialog for user.

####**ThreadedClient**: A class for implementing asynchronous UI.
**__init__(self, master)**: Launch the main part of the GUI and the worker thread. periodicCall an endApplication could reside in the GUI part, but putting them here means that you have all the thread controls in a single place.

**periodicCall(self)**: Check every 100 ms if there is something new in the queue.

**workerThread1(self)**: This is where we handle the asynchronous I/O. For example, it may be a 'select()'. One important thing to remember is that the thread has to yield control.

**endApplication(self)**: Close the whole UI.

###*AutoEMR.py*: Speech recognition and text classification is done in this file, result of classification will be written in *data/text.txt* for the UI to read.

**Vote(text)**: For a sentence as the input parameter, it will call both Basic mode and Advanced mode and generate a voting result of these algorithms as its output.

**HardClassify(text)**: Basic Mode, taking a sentence as its input parameter, classify it and generate the classification result as its output(using decision tree and naive bayes algorithms).

**MLClassify(text)**: Advanced Mode, taking a sentence as its input parameter, classify it and generate the classification result as its output(using machine learning algorithm).

**Recogize(audio)**: Taking a voice file as its input, send it to the Google server and get the speech-recognition result. The output is the marked result text sentence.

**OutputSingle()**: Write the first sentence from the queue into the pipeline file(for UI to read), also, detect whether the conversation should be terminate.

**OutputWhole(log)**: Called when the conversation ends. It will output the whole conversation to the terminal(for debug).

**Main**: Train the machine learning model, generate objects for speech_recognition API, create processes for recording.


###*MLtesting.py*: A lite test version for machine learning model that works without microphones and UI. You can use this file to test modify the ML model during development, not for release.







This is the modified version, if you want to check our original project, please check the following page:
https://github.com/FalsitaFine/Senior-Design

