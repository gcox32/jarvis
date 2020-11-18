from gtts import gTTS
import speech_recognition as sr
import os
import webbrowser
import smtplib

def talkToMe(audio):
    print(audio)
    tts = gTTS(text = audio, lang = 'en-uk')
    tts.save('audio.mp3')
    os.system('afplay audio.mp3')

# listen for commands

def myCMD():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('I am ready and listening.')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration = 1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        command = str(command).lower()
        print('You said {} \n'.format(command))
    
    # loop back to continue to listen for commands
    except sr.UnknownValueError:
        assistant(myCMD())

    return command

def assistant(command):
    if 'how are you' in command:
        talkToMe('Well, sir.')


talkToMe('Ready, sir.')

while True:
    assistant(myCMD())