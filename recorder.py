import speech_recognition as sr
 
def listen(recognizer):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = recognizer.listen(source, phrase_time_limit=5)
        return audio

def transcript(recognizer, audio):
# Speech recognition using Google Speech Recognition
    try:
        speech = recognizer.recognize_google(audio, language='pt')
        return speech
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

if __name__ == '__main__':
    recognizer = sr.Recognizer()
    audio = listen(recognizer)
    speech = transcript(recognizer, audio)
    print(speech)
