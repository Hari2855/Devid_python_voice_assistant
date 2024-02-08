import pyttsx3
import speech_recognition as sr
# import pyaudio
import datetime
import os
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QObject, QTimer, QTime,  QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisUi import Ui_jarvisUi
import requests
from bs4 import BeautifulSoup
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    strTime = datetime.datetime.now().strftime("%I:%M %p")
    tt = strTime
    search = "temperature in mumbai"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div",class_="BNeawe").text

    if hour>=0 and hour<=12:
        speak(f"Good Morning sir")
        speak(f"Its {tt} and temperature is {temp}")
        speak('I am Devid sir. please tell me how can i help you')

    elif hour>12 and hour<18:
        speak("Good Afternoon sir")
        speak(f"Its {tt} and temperature is {temp}")
        speak('I am Devid sir. please tell me how can i help you') 

    else:
        speak("Good Evening sir")
        speak(f"Its {tt} and temperature is {temp}")
        speak('I am Devid sir. please tell me how can i help you')

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youe email', 'your password')
    server.sendmail('your email', to, content)
    server.close()


class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()
 
    def run(self):
        self.TaskExecution()

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening....")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=60, phrase_time_limit=10)
            
        try:
            print("Recognizing....")
            self.query = r.recognize_google(audio, language='en-in')
            print(f"sir said: {self.query}")
            print("Executing command....")

        except Exception as e:
            speak('Sorry, I could not understand. Could you please say that again?')
            return "none"
        self.query = self.query.lower()
        return self.query
    
    def TaskExecution(self):
            wish()
            while True:
                self.query = self.takecommand().lower()

                if "open notepad" in self.query:
                    npath = "C:\\Windows\\notepad.exe"
                    os.startfile(npath)

                elif 'open command prompt' in self.query:
                    os.system('start cmd')

                elif 'open camera' in self.query:
                    cap = cv2.VideoCapture(0)
                    while True:
                        ret, img = cap.read()
                        cv2.imshow('webcam', img)
                        k = cv2.waitKey(50)
                        if k==27:
                            break
                    cap.release()
                    cv2.destroyAllWindows()

                elif 'time' in self.query:
                     strTime = datetime.datetime.now().strftime("%I:%M %p")
                     speak(f'Sir, the time is {strTime}')
                     tt = strTime

                elif 'hello' in self.query:
                    speak('Hello sir may I help you with something')

                elif 'remember that' in self.query:
                    speak("what should i remember sir")
                    rememberMessage = self.takecommand().lower()
                    speak("you said me to remember"+rememberMessage)
                    remember = open('data.txt', 'w')
                    remember.write(rememberMessage)
                    remember.close()

                elif 'do you remember anything' in self.query:
                    remember = open('data.txt', 'r')
                    speak("you said me to remember that" + remember.read())
                
                elif 'how are you' in self.query or 'how r u' in self.query:
                    speak('I am fine and full of energy')
                    speak('What about you sir?')

                elif 'temperature' in self.query or 'weather' in self.query:
                    search = "temperature in mumbai"
                    url = f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text, "html.parser")
                    temp = data.find("div",class_="BNeawe").text
                    speak(f"current {search} is {temp}")




                elif 'i am fine' in self.query or 'i am good' in self.query or 'i m fine' in self.query or 'i m good' in self.query:
                    speak('Its good to know that you are fine')

                elif 'who created you' in self.query:
                    speak('I have been created by Hari sir')
        
                elif 'play music' in self.query:
                    speak('Ok sir')
                    musuc_dir = "C:\\Users\Sachi\\Music"
                    songs = os.listdir(musuc_dir)
                    rd = random.choice(songs)
                    os.startfile(os.path.join(musuc_dir, rd))

                elif 'ip address' in self.query:
                    print("Checking....")
                    ip = get('https://api.ipify.org').text
                    speak(f"your IP address is {ip}")

                elif "wikipedia" in self.query:
                    speak('Searching wikipedia...')
                    self.query = self.query.replace("Wikipedia", "")
                    results = wikipedia.summary(self.query, sentences=2)
                    speak("According to wikipedia...")
                    speak(results)
                    print(results)

                elif 'open vs code' in self.query:
                    speak('Ok sir')
                    pat = "C:\\Users\\Sachi\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                    os.startfile(pat)

                elif 'open youtube' in self.query:
                    speak('Ok sir')
                    webbrowser.open('www.youtube.com')
        
                elif 'open facebook' in self.query:
                    speak('Ok sir')
                    webbrowser.open('www.facebook.com')

                elif 'open google' in self.query:
                    chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
                    speak('Ok sir, what should I search on google?')
                    cm = self.takecommand()
                    webbrowser.get('chrome').open(f"https://www.google.com/search?q={cm}")

                elif 'send message' in self.query:
                    speak('what you want to say in message?')
                    me = self.takecommand().lower()
                    kit.sendwhatmsg("phone number with +91", me, 2,25)

                elif 'play song on youtube' in self.query:
                    speak("Ok sir, enjoy....")
                    kit.playonyt("albeli ne")

                elif 'email' in self.query:
                    speak('Ok sir')
                    try:
                        speak("What should i say?")
                        content = self.takecommand().lower()
                        to = "Emai on which you want to send"
                        sendEmail(to, content)
                        speak("Email has been sent.")
                    except Exception as e:
                        print(e)
                        speak("sorry sir, I am not able to send this email at this time")

                elif 'by' in self.query:
                    speak('Ok sir by ,  I am always ready for your help.')
                    sys.exit()
                
                elif "wait" in self.query or "sleep" in self.query:
                   speak("Ok sir, I am going to sleep for 1 minute.")
                   time.sleep(60)
                   speak("I am awake now. How can I help you, sir?")
                    
                    
                else:
                  chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                  webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
                  speak('Sorry, I do not understand. Let me search it for you.')
                  webbrowser.get('chrome').open(f"https://www.google.com/search?q={self.query}")
                  
time.sleep(10)


startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_jarvisUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:/Jarvis/back.jpg")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Jarvis/7cbd1ea0813d9861452e3b88493d5642.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Jarvis/loa.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Jarvis/gf.gif")
        self.ui.label_5.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Jarvis/be92f51ef908d53c0c74d5e06a59365e.gif")
        self.ui.label_6.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Jarvis/ezgif-1-0bc8cdba2b.gif")
        self.ui.label_7.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Jarvis/54f8e332b488dfdb2d3cc2efce8a536a.gif")
        self.ui.label_8.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())