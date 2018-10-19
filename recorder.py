import speech_recognition as sr
import sys
import argparse
import io
from pydub import AudioSegment
from google.cloud import speech


def listen_from_file(path):
    audio_file = AudioSegment.from_wav(path)
    audio_file = audio_file.set_channels(1)
    audio_file.export('audio_file.wav', format='wav')
    return audio_file

def listen(recognizer):
    with sr.Microphone() as source:
        #recognizer.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = recognizer.listen(source, phrase_time_limit=30)
        f = open('audio_file.wav', 'wb')
        f.write(audio.get_wav_data())

def transcript(path):
    client = speech.SpeechClient()
    if path:
        audio_file = listen_from_file(path)
    else:
        audio_file = listen(sr.Recognizer())
    with open('audio_file.wav', 'rb') as audio_file:
        content = audio_file.read()

    
    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code='pt-BR',
        use_enhanced=True,
        enable_automatic_punctuation=True,
        #audio_channel_count=1,
        #enable_separate_recognition_per_channel=True,
        model='command_and_search')

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print('Transcript: {}'.format(alternative.transcript))

if __name__ == '__main__':
    path = None
    if (len(sys.argv) > 1):
        path = sys.argv[1]
    transcript(path=path)
