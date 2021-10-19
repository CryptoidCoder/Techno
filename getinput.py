import pyttsx3 # for text-to-speech
import webbrowser #for opening web pages
import smtplib #for emailing
import random # to pick random
import speech_recognition as s_r #for speech-to-text
import wikipedia #to look stuff up
import datetime #to find the date+time
import os # to open programs
import sys # to use the system
import time #so you can wait

from pynput.keyboard import Key, Controller, Listener #to use the media keys
from dotenv import load_dotenv
import requests #to send web requests


load_dotenv()


#setup pynput
pynputkeyboard = Controller()

# Initialize speech 
engine = pyttsx3.init('sapi5')


#set the username
Master = os.getenv('Master')

#what voice the text to speech will use
american = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0" #Path to the american voice
british = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0" #Path to the british voice
speakingvoice = british # default speaking voice is british


wakeword = os.getenv('WakeWord')

#set the speaking engine
voices = engine.getProperty('voices')
#set the words per minute rate of speech engine
engine.setProperty('voice', speakingvoice)

def addnewline(filename,text): #append text to a new line on a file
    # Open the file in append & read mode ('a+')
    with open(filename, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text)
        file_object.close()

def listening(mode, value): #turn a LED / printout something if mic is listening
    if mode == 'silent':
        if value == True:
            print() #turn on LED
            addnewline('ledfunctions.log', f"{datetime.datetime.now()}, {mode}, {value}")

        else:
            print() # turn off LED
            addnewline('ledfunctions.log', f"{datetime.datetime.now()}, {mode}, {value}")

    elif mode == 'message':
        if value == True:
            printspeak("Listening...")
            addnewline('ledfunctions.log', f"{datetime.datetime.now()}, {mode}, {value}")
        else:
            printspeak("No Longer Listening.")
            addnewline('ledfunctions.log', f"{datetime.datetime.now()}, {mode}, {value}")


def justspeak(audio): # speak what is inputed
    engine.say(audio)
    engine.runAndWait()

def printspeak(text): # speak and print what is inputed
    print(text)
    engine.say(text)
    engine.runAndWait()

def greetMe(): #say either good morning, good afternoon or good evening depending on the time.
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        printspeak(f'Good Morning {Master}!')

    if currentH >= 12 and currentH < 18:
        printspeak(f'Good Afternoon {Master}!')

    if currentH >= 18 and currentH !=0:
        printspeak(f'Good Evening {Master}!')

def myCommand(): #turn sound into text
    r = s_r.Recognizer()
    my_mic = s_r.Microphone(device_index=1) #my device index is 1, you have to put your device index
    try:
        with my_mic as source:
            listening('message', True)
            r.adjust_for_ambient_noise(source) #reduce noise
            audio = r.listen(source) #take voice input from the microphone
            listening('message', False)
            query = (r.recognize_google(audio))
            query = query.lower()
            log(query)

    except:
        printspeak("Error taking in audio.") 
    
    return query

def log(query): #output datetime, query to query.log file
    datetimenow = datetime.datetime.now()
    datetimenow = str(datetimenow)
    message = "At Time: " + datetimenow + f" {wakeword} Recieved: " + query
    addnewline("query.log",message)
    return message

def fetchlog(): #get latest query from query.log file
    with open('query.log', 'r') as f:
        last_line = f.readlines()[-1]
        query = last_line[53:]
        return query

def startup(): #what to do on startup
    greetMe()
    printspeak(f"Hello My Name is {wakeword}, Your Virtual Helper.")
    #query = myCommand()


startup()


loop = True
while loop == True:
    while loop == True: #when wakeword spoke, take query input & save it

        r = s_r.Recognizer()
        my_mic = s_r.Microphone(device_index=1) #my device index is 1, you have to put your device index
        try:
            with my_mic as source:
                listening('silent', True)
                r.adjust_for_ambient_noise(source) #reduce noise
                audio = r.listen(source) #take voice input from the microphone
                listening('silent', False)
            query = (r.recognize_google(audio))
            query = query.lower()
            if wakeword in query:
                printspeak("WakeWord Activated")
                break

            if 'exit' in query or 'stop' in query or 'end' in query or 'cancel' in query:
                printspeak("Exiting Session...")
                loop = False

        except:
            print("No Wakeword...")

    if loop == True:
        myCommand()
        printspeak("Processing...")
        import processquery
    
    else:
        loop = False

    