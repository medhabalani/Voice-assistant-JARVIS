from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import datetime
import time
import pyjokes
import pyttsx3
import pywhatkit
import randfacts
import speech_recognition
import wikipedia
import weathercom
import json

speaker = pyttsx3.init()
listener = speech_recognition.Recognizer()
tones = speaker.getProperty('voices')
speaker.setProperty('voice', tones[1].id)


# def get_info(query):
#     driver = webdriver.Chrome(ChromeDriverManager().install())
#     driver.get(url="https://www.wikipedia.org/")
#     search = driver.find_element_by_xpath('//*[@id="searchInput"]')
#     search.click()
#     search.send_keys(query)
#     enter = driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/button/i')
#     enter.click()


def get_review(query):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url="https://www.google.com/")
    driver.find_element_by_name("q").send_keys(query + " imdb")
    # time.sleep(1)
    driver.find_element_by_name("btnK").send_keys(Keys.ENTER)
    # driver.implicitly_wait(20)
    driver.find_element_by_tag_name("cite").click()
    # driver.implicitly_wait(20)
    info = driver.find_element_by_class_name('ratingValue')
    imdb = info.text
    return imdb


def weatherReport(city):
    weatherDetails = weathercom.getCityWeatherDetails(city)
    humidity = json.loads(weatherDetails)["vt1observation"]["humidity"]
    temp = json.loads(weatherDetails)["vt1observation"]["temperature"]
    phrase = json.loads(weatherDetails)["vt1observation"]["phrase"]
    return humidity, temp, phrase


def respond(text):
    speaker.say(text)
    speaker.runAndWait()


def instruct_me():
    try:
        with speech_recognition.Microphone() as user_voice:
            speaker.say("How can I help you ?")
            speaker.runAndWait()
            voice = listener.listen(user_voice)
            prompt = listener.recognize_google(voice)
            prompt = prompt.lower()
            if 'alexa' in prompt:
                prompt = prompt.replace('alexa', '')



    except Exception as e:
        print(e)
        respond("Unable to Recognize your voice.")
        return "None"
    return prompt


def instruct_me_2():
    try:
        with speech_recognition.Microphone() as user_voice:
            voice = listener.listen(user_voice)
            prompt = listener.recognize_google(voice)
            prompt = prompt.lower()
            return prompt
    except:
        pass


def start():
    prompt = instruct_me()
    if 'who are you' in prompt:
        respond('I am your voice assistant!')
    elif 'how are you' in prompt:
        respond("I am fine, Thank you")
        respond("How are you, Sir")
    elif 'wish me' in prompt:
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            respond("Good Morning Sir !")
        elif 12 <= hour < 18:
            respond("Good Afternoon Sir !")
        else:
            respond("Good Evening Sir !")
        respond('I am your assistant created by Medha!')
    elif 'who made you' in prompt:
        respond('Medha from triple I T Allahabad made me , but how did she got time from her busy sleeping schedule!')
    elif 'time' in prompt:
        respond(datetime.datetime.now().strftime('%I:%M %p'))
    elif 'play' in prompt:
        song = prompt.replace('play', '')
        respond('playing' + song)
        pywhatkit.playonyt(song)
    elif 'fact' in prompt:
        respond(randfacts.getFact())
    elif 'joke' in prompt:
        respond(pyjokes.get_joke())
    elif 'who is' in prompt:
        human = prompt.replace('who is', '')
        respond(wikipedia.summary(human, 2))
    elif 'what is a' in prompt:
        thing = prompt.replace('what is a', '')
        respond(wikipedia.summary(thing, 2))
    elif "what is the weather today" in prompt:
        respond("which city")
        city = instruct_me_2()
        humidity, temp, phrase = weatherReport(city)
        respond("currently in " + city + "  temperature is " + str(temp)
                + " degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase)
    elif 'movie rating' in prompt:
        movie = prompt.replace('movie rating', '')
        imdbb = get_review(movie)
        imdbb = imdbb.split("/")
        respond('It has I M B D rating' + imdbb[0])
    else:
        respond('Please say again !')


while True:
    start()
