import speech_recognition as sr


r = sr.Recognizer()

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source=source)
    audio = r.listen(source, timeout=3)

data = ''
try:
    data = r.recognize_google(audio)
    print(data)

except sr.UnknownValueError:
    print(" Error")

except sr.RequestError as e:
    print("Request Error")