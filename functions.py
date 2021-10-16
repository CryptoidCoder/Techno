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
from pynput.keyboard import Key, Controller #to use the media keys
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


#set the speaking engine
voices = engine.getProperty('voices')
#set the words per minute rate of speech engine
engine.setProperty('voice', speakingvoice)


def justspeak(audio): #definition to just speak what is inputed: justspeak(what you want him to say)
    engine.say(audio)
    engine.runAndWait()

def printspeak(text): #definition to speak and print what is inputed: printspeak(what you want him to say and print)
    print(text)
    engine.say(text)
    engine.runAndWait()

def greetMe(): #say either good morning, good afternoon or good evening depending on the time.
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        printspeak('Good Morning!')

    if currentH >= 12 and currentH < 18:
        printspeak('Good Afternoon!')

    if currentH >= 18 and currentH !=0:
        printspeak('Good Evening!')

def myCommand():
    r = s_r.Recognizer()
    my_mic = s_r.Microphone(device_index=1) #my device index is 1, you have to put your device index
    with my_mic as source:
        printspeak("Listening...")
        r.adjust_for_ambient_noise(source) #reduce noise
        audio = r.listen(source) #take voice input from the microphone
    #printspeak(r.recognize_google(audio)) #to print voice into text
    query = (r.recognize_google(audio))
    return query.lower()


query = myCommand()
print(query)