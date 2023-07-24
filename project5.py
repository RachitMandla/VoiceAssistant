import subprocess
import pyttsx3
import smtplib
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import time
import threading
import tkinter as tk
from PIL import ImageTk, Image
import requests
import json
from tkinter import ttk


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        text_entry.delete(0, tk.END)
        text_entry.insert(tk.END, text)
    except sr.UnknownValueError:
        text_entry.delete(0, tk.END)
        text_entry.insert(tk.END, "Unable to recognize speech.")
    except sr.RequestError:
        text_entry.delete(0, tk.END)
        text_entry.insert(tk.END, "Speech recognition request error.")


def speak():
    text = text_entry.get()
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Welcome to voice assistant. Please tell me how may I help you")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        input = r.recognize_google(audio, language='en-in')
        print(f"User said: {input}\n")

    except Exception as e:
        print("Say that again please...")
        return "None"
    return input


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('viproject.404@gmail.com', 'jyrobzamfbhwrurd')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()


def get_weather(city):
    api_key = "65197d5100f28d4c13846032da13e98f"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(base_url)
    weather_data = json.loads(response.text)

    if weather_data["cod"] != "404":
        main_info = weather_data["weather"][0]["main"]
        description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]

        # Convert temperature from Kelvin to Celsius
        temperature_celsius = temperature - 273.15

        weather_info = f"The weather in {city} is {main_info} ({description}). " \
                       f"The temperature is {temperature_celsius:.2f} degrees Celsius and the humidity is {humidity}%."
        speak(weather_info)
    else:
        speak("City not found. Please try again.")


def run_voice_assistant():
    wishMe()
    while True:
        input = takeCommand().lower()

        if 'wikipedia' in input:
            speak('Searching Wikipedia...')
            input = input.replace("wikipedia", "")
            results = wikipedia.summary(input, sentences=4)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in input:
            webbrowser.open("youtube.com")

        elif 'open google' in input:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in input:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in input:
            music_dir = 'C:\\Users\\Lenovo\\OneDrive\\Desktop\\project5\\source\\MUSIC'

            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in input:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f" the time is {strTime}")

        elif 'email to me' in input:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "projectvi404@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry. I am not able to send this email")

        elif 'weather' in input:
            speak("Please say the name of the city.")
            city = takeCommand()
            get_weather(city)

        elif 'exit' in input:
            speak("Thanks for giving me your time")
            exit()

        elif "log off" in input or "sign out" in input:
            speak("Make sure all the applications are closed before signing out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])

        elif 'shutdown system' in input:
            speak("Hold On a Sec! Your system is on its way to shut down")
            subprocess.call('shutdown /p /f')

        elif "restart" in input:
            subprocess.call(["shutdown", "/r"])


def start_listening():
    threading.Thread(target=run_voice_assistant).start()





# Create the main window
window = tk.Tk()
window.title("Voice Assistant")
window.geometry("400x500")
window.configure(background="black")

# Create the text entry widget
text_entry = tk.Entry(window, width=30, bd=0)
text_entry.pack(pady=10)

# Modify the text entry widget's background color
text_entry.configure(bg="white")

# Create a frame for the microphone button and line
frame = tk.Frame(window, bg="black")

# Load the microphone image and resize it
microphone_img = ImageTk.PhotoImage(
    Image.open("mic.png").resize((90, 100), Image.ANTIALIAS)
)

mic_button = tk.Button(frame, image=microphone_img, command=start_listening, bd=0, bg="black", relief="flat")
mic_button.pack(side=tk.BOTTOM, pady=(0, 5))

line_canvas = tk.Canvas(frame, width=500, height=1, bg="black", highlightthickness=0)
line_canvas.pack(side=tk.TOP)

line_canvas.create_line(10, 1, 400, 1, fill="#555555", width=2)
line_canvas.create_line(10, 2, 400, 2, fill="#999999", width=2)

# Pack the frame at the bottom of the window
frame.pack(side=tk.BOTTOM)
# Start the main loop
window.mainloop()
