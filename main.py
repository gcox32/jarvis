import os
from service import Service, find_syslog
import time
import logging
from logging.handlers import SysLogHandler
from gtts import gTTS
import speech_recognition as sr

class Jarvis(Service):
    def __init__(self, filepath = '/Users/administrator/projects/Independent/jarvis/', *args, **kwargs):
        super(Jarvis, self).__init__(*args, **kwargs)
        self.logger.addHandler(SysLogHandler(address=find_syslog(),facility=SysLogHandler.LOG_DAEMON))
        self.logger.setLevel(logging.INFO)
        self.filepath = filepath
        # self.talk('Ready, sir.')
        self.checkin()


    def checkin(self):
        pass

    def talk(self, audio):
        print(audio)
        tts = gTTS(text = audio, lang = 'en-uk')
        audiopath = self.filepath + 'audio/audio.mp3'
        tts.save(audiopath)
        os.system(f'afplay {audiopath}') 
    
    def assistant(self, command):
        if 'how are you' in command:
            self.talk('Well, sir.')
        if 'do this' in command:
            self.talk('Right away, sir.')
        if 'shut down' in command:
            self.talk('shutting down, sir.')
            self.stop()

    def mycommand(self):

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
            cmd = self.mycommand()
            self.assistant(cmd)

        return command

    def run(self):
        while not self.got_sigterm():
            self.logger.info("I'm working...")
            time.sleep(5)

            # listening loop
            self.assistant(self.mycommand())

    def stop(self, block=False):
        print('shutting down, sir.')
        return super().stop(block=block)

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        sys.exit('Syntax: {} COMMAND'.format(sys.argv[0]))
    cmd = sys.argv[1].lower()
    service = Jarvis(name = 'jarvis', pid_dir = '/tmp')

    if cmd == 'start':
        service.start()

    elif cmd == 'stop':
        service.stop()
    elif cmd == 'status':
        if service.is_running():
            print("I'm running, sir.")

        else:
            print("I'm not currently running, sir")
    else:
        sys.exit("I'm not sure what to do with your instruction: {}".format(cmd))

    