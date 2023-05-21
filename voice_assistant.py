import datetime
import easyocr
import numpy as np
import pyttsx3
import speech_recognition as sr


commands_list = {
    'say_time()': [
        'która godzina',
        'jaki mamy czas',
        'która jest',
        'jaki jest czas'
    ],
}
WAKE = 'janko'


def speak(text: str):
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.say(text)
    engine.runAndWait()

def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

        try:
            said = recognizer.recognize_google(audio, language='pl-PL')
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
            return 'NOT UNDERSTOOD'
        except sr.RequestError as e:
            print('Could not request results from Google Speech Recognition service:', str(e))
            return 'ERROR'

    return said.lower()


def greetings():
    speak(f'Nazywam się Janka. Jestem asystentem głosowym. Jeśli będziesz mnie potrzebował, zawołaj mnie: {WAKE}')


def validate_text(text):
    match text:
        case 'NOT UNDERSTOOD':
            speak('Nie zrozumiałam.')
            return 0
        case 'ERROR':
            speak('Wystąpił błąd. Nie wiem co się dzieje.')
            return 0
        case _:
            return text

def listen():
    text = get_audio()

    if text.count(WAKE) > 0:
        speak('Tak?')
        text = validate_text(get_audio())

        if text:
            if 'wyłącz się' in text:
                speak('Żegnam ozięble.')
                return 0
            else:
                command_to_type = ''
                if commands_list['type(text)'][0] in text:
                    index_to_type = text.index(commands_list['type(text)'][0])
                    command_to_type = text[index_to_type:]
                    text = text[:index_to_type]

                commands_split = text.split(' i ')
                commands = [command for command in commands_split if len(command)]

                if len(command_to_type):
                    commands.append(command_to_type)

                for command in commands:
                    result = execute_command(command)

                    if not result:
                        speak(f'Nie znalazłam akcji dla: {command}')

    return 1

def execute_command(text):
    for key, value in commands_list.items():
        for v in value:
            if v in text:
                exec(f'{key}')
                return 1

    return 0


def say_time():
    time_now = str(datetime.datetime.now().time()).split(':')
    hour = int(time_now[0])
    minutes = time_now[1]
    text = ''

    match hour:
        case 0:
            text += 'zero '
        case 4 | 5 | 6 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20:
            text += f'{hour}-ta '
        case 1 | 21:
            text += f'{hour}-sza '
        case 2 | 22:
            text += f'{hour}-ga '
        case 3 | 23:
            text += f'{hour}-cia '
        case 7 | 8:
            text += f'{hour}-ma '

    text += minutes

    speak(text)

def say_wakeup_news():
    pass
    # TODO: Prepare string for wake up news including day, weekday, time and weather:
    # Dzień dobry. Jest 18 maja. Czwartek. Godzina 6:50. Pogoda na dziś: opis pogody