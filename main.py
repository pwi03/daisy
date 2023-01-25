import time

import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import simpleaudio as sa # pipwin install simpleaudio
import speech_recognition as sr   # pip install SpeechRecognition
# pip install pipwin ----> pipwin install PyAudio

r = sr.Recognizer() # initialize recognizer
# initialize audios
ansprechbar = "audio\\06.wav"
stabile_seitenlage = "audio\\09.wav"
blut = "audio\\10.wav"
#wiederholen = "audios\\wiederholen.wav"
lehrkraft = "audio\\02.wav"
atmen = "audio\\07.wav"
strom_feuer = "audio\\04.wav"
einleitung = "audio\\01.wav"
notaus = "audio\\05.wav"
sekretariat = "audio\\03.wav"
wiederbeleben = "audio\\08.wav"
beruhigen = "audio\\13.wav"
blutung_abdruecken = "audio\\11.wav"
lehrkraft_warten = "audio\\12.wav"
lied_hlw = "audio\\biene_maja.wav"
beep = "audio\\beep.wav"
#
MyText = "START"

alertid = ""

cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

serverToken = 'AAAAv3RiIFQ:APA91bE0i2Atdh45zJr-lJ97x4ZmKA5On-j0LL8VelDLKS62ER0LhFWq4dGtI4FoZM1E0JpyUfV-jcE3Xnko_J54bHsnhweZk5dnw4w7o-mCs7wO7AHBfbhE9Ohkvu3JM9Ac6suIrPj_'

headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
      }

def createAlert(alert, place, q1):
    Obj1 = {
        'from': 'DSP',
        'place': place,
        'q1': q1,
        'status': '1'
    }

    data = [Obj1]

    for record in data:
        doc_ref = db.collection(u'emergencies').document(alert)
        doc_ref.set(record)

def playAudio(MyAudio):
    wave_obj = sa.WaveObject.from_wave_file(MyAudio) #take audio
    play_obj = wave_obj.play() #play audio
    play_obj.wait_done()

def playBeep():
    wave_obj = sa.WaveObject.from_wave_file(beep) #take audio
    play_obj = wave_obj.play() #play audio

def checkStop(MyText):
    if MyText.lower() == "stopp" or MyText.lower() == "halt" or MyText.lower() == "ende" or MyText.lower() == "aus":
        return True


def getAnswer():
    MyText = "START"
    with sr.Microphone() as source2:  # micro as input
        r.adjust_for_ambient_noise(source2, duration=0.2)  # adjust to backround noises
        playBeep()
        audio2 = r.listen(source=source2, phrase_time_limit=3)  # listen to input(user talk)
    try:
        MyText = r.recognize_google(audio2, language="de-DE")  # using google to recognize, german as language
        MyText = MyText.lower()
        print(MyText)
        if checkStop(MyText):
            return "STOP"
    except Exception as e:  # errorhandling
        print(e)
    wdh = True
    while wdh:
        if MyText == "":
            MyText = "ERROR"
        if MyText == "ja":
            return "ja"
        elif MyText == "nein":
            return "nein"
        else:
            print("wdhx")
            #playAudio(wiederholen)
            playBeep()
            with sr.Microphone() as source2:  # micro as input
                r.adjust_for_ambient_noise(source2, duration=0.2)  # adjust to backround noises
                audio2 = r.listen(source=source2, phrase_time_limit=3)  # listen to input(user talk)
            try:
                MyText = r.recognize_google(audio2, language="de-DE")  # using google to recognize, german as language
                MyText = MyText.lower()
                print(MyText)
                if checkStop(MyText):
                    return "STOP"
            except Exception as e:
                print(e)




def startDaisy(room):
    #EINLEITUNGSAUDIO
    #playAudio(einleitung)
    ##########
    #IST EINE LEHRKRAFT ANWESEND?
    ##########



    playAudio(lehrkraft)

    answer = getAnswer()

    if answer == "STOP":
        return
    elif answer == "nein":
        alertid = room + "" + str(round(time.time()))
        createAlert(alertid, room, 0)

        body = {
            'notification': {'body': alertid,
                             'title': '** Notfall! ** Ort: ' + room + ' **'
                             },
            'to':
                '/topics/alerts',
            'priority': 'high',
            #   'data': dataPayLoad,
        }
        response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
        print(response.status_code)
        print("Done")


        playAudio(sekretariat)

    playAudio(strom_feuer)

    answer = getAnswer()

    if answer == "STOP":
        return
    elif answer == "ja":
        playAudio(notaus)

    playAudio(ansprechbar)

    answer = getAnswer()

    if answer == "STOP":
        return
    elif answer == "ja":
        playAudio(beruhigen)
        playAudio(blut)
        answer = getAnswer()
        if answer == "STOP":
            return
        elif answer == "ja":
            playAudio(blutung_abdruecken)
        playAudio(lehrkraft_warten)
    elif answer == "nein":
        playAudio(atmen)
        answer = getAnswer()
        if answer == "STOP":
            return
        elif answer == "ja":
            playAudio(stabile_seitenlage)
        elif answer == "nein":
            while 1 == 1:
                playAudio(wiederbeleben)
                playAudio(lied_hlw)

while True:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIU.PUD_UP)
    starting = True
    playBeep()
    while starting == True:
        if (GPIO.input(15)==True):
            starting = False
    startDaisy("E109")
