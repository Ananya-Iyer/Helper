'''
TO-DO
1) adding text to speech service
2) opening web browsers in the same audio instead of passing a second audio
3) Debug why maya 2018 and 2016 are opening together
4) improvise on listening
'''

import json
from logging import PlaceHolder
import os
import sys
import time
import datetime
import re
import json
import subprocess
import pyttsx3
import wikipedia
import speech_recognition as sr
import webbrowser as browser

r1 = sr.Recognizer()
microphone = sr.Microphone()
listening = False
pre_defined_commands = ("start application", "shutdown")
user_init_file_path = f"C:/temp/{os.environ['USERNAME']}"
user_info_dict = {'username': '', 'botname': ''}
# Keywords
# actions = ('open', 'close', 'search')
# commands = ('run', )

def user_initializations():
    USER_NAME = input("Hi User. Please Enter your name : \n")
    user_info_dict["username"] = USER_NAME
    BOT_NAME = input(f"Hi {USER_NAME}. I'm your buddy. By what name would you like to call me ? \n")
    user_info_dict["botname"] = BOT_NAME
    if not os.path.exists(user_init_file_path):
        os.makedirs(user_init_file_path)

    with open (f"{user_init_file_path}/user_settings.json", "w") as writer:
        json.dump(user_info_dict, writer, indent=4)


class HelperMain(object):

    if not os.path.exists(f"{user_init_file_path}/user_settings.json"):
        user_initializations()
    with open(f"{user_init_file_path}/user_settings.json", "r") as reader:
        user_info = json.load(reader)
    user_name = user_info["username"]
    bot_name = user_info["botname"]

    voice_engine = pyttsx3.init("sapi5")
    voice_engine.setProperty("voices", voice_engine.getProperty("voices")[0].id)
    def __init__(self):
        object.__init__(self)
        self.helper_greeting_startup()

    def helper_speak(audio):
        '''
        Helps to set up the voice of bot
        '''
        HelperMain.voice_engine.say(audio)
        HelperMain.voice_engine.runAndWait()

    def helper_greeting_startup(self):
        '''
        runs at every time the program is killed and its restarted
        '''
        hours = int(datetime.datetime.now().hour)
        if hours >=0 and hours <12:
            HelperMain.helper_speak(f"Hi Good morning {HelperMain.user_name} ! How are you today")
        elif hours >=12 and hours <16:
            HelperMain.helper_speak(f"Hi Good afternoon {HelperMain.user_name} ! How are you today")
        else:
            HelperMain.helper_speak(f"Hi Good evening {HelperMain.user_name} ! How are you today")

        HelperMain.helper_speak(f"I am {HelperMain.bot_name}. What can I do for you")

    def command_to_helper():
        with microphone as audio_source:
            r1.adjust_for_ambient_noise(audio_source, 10)
            print("Listening...")
            r1.pause_threshold = 1
            audio = r1.listen(audio_source)
        try:
            query = r1.recognize_google(audio, language='en-in').lower()
            print(query)

        except Exception as e:
            print("Couldn't process your query. Exception occured {e}")
            return "None"
        return query
        
    def processing_query(query):
        action = query.lower()
        if re.search(".*notepad*", action):
            HelperMain.helper_speak("Ok, Opening Notepad .....")
            p = subprocess.Popen("C:/Windows/System32/notepad.exe")

        if re.search(".*maya.*2018*", action):
            HelperMain.helper_speak("Ok, Opening Maya 2018 .....")
            p = subprocess.Popen("C:/Program Files/Autodesk/Maya2018/bin/maya.exe")

        if re.search(".*maya.*2016*", action):
            HelperMain.helper_speak("Ok, Opening Maya 2016 .....")
            p = subprocess.Popen("C:/Program Files/Autodesk/Maya2016.5/bin/maya.exe")

        if re.search(".*wikipedia*", action):
            HelperMain.helper_speak("Searching in Wikipedia .....")
            action = action.replace("wikipedia", "")
            results = wikipedia.summary(action, sentences=2)
            HelperMain.helper_speak("According to wikipedia")
            HelperMain.helper_speak(results)

        # if re.search('youtube', action):      
        #     # browser.get().open_new('https://www.youtube.com/results?search_query=python')
        #     with microphone as sub_audio:
        #         r2 = sr.Recognizer()
        #         print('search a video of?')
        #         sub_audio = r2.listen(sub_audio)
        #         try:
        #             sub_action = r2.recognize_google(sub_audio)
        #             browser.get().open_new(f'https://www.youtube.com/results?search_query={sub_action}')
        #         except sr.RequestError as e:
        #             print('couldnt open youtube video')


        # if 'shutdown' in recognizer.recognize_google(audio):
        #     try:
        #         print('shutting down pc')
        #         os.system("shutdown /f /t 1")
        #     except sr.RequestError as e:
        #         print('couldnt shutdown. Exception occured {e}')

        # if 'restart' in recognizer.recognize_google(audio):
        #     try:
        #         print('restarting system')
        #         os.system("shutdown /r /f /t 1")
        #     except sr.RequestError as e:
        #         print('couldnt restart. Exception occured {e}')

        # if 'log off' in recognizer.recognize_google(audio):
            # try:
            #     print('logging off')
            #     os.system("shutdown /l")
            # except sr.RequestError as e:
            #     print('couldnt sign you out. Exception occured {e}')

    # stop_listening = r1.listen_in_background(microphone, command_to_helper, phrase_time_limit=10)
    # while 1:
    #     time.sleep(0.1)

    # stop_listening(wait_for_stop=False)

if __name__ == "__main__":
    HelperMain()
    while 1:
        query = HelperMain.command_to_helper()
        HelperMain.processing_query(query=query)
