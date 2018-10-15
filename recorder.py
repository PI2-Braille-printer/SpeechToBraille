import speech_recognition as sr
import sys
import argparse
import io
from pydub import AudioSegment
from google.cloud import speech


def listen_from_file(path):
    audio_file = AudioSegment.from_wav(path)
    audio_file = audio_file.set_channels(1)
    audio_file.export('tmp.wav', format='wav')
    return audio_file

def listen(recognizer):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = recognizer.listen(source, phrase_time_limit=5)
        return audio

def transcript(path):
    client = speech.SpeechClient()
    audio_file = listen_from_file(path)
    
    with io.open('tmp.wav', 'rb') as audio_file:
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
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('path', help='File to stream to the API')

    args = parser.parse_args()

    transcript(args.path)
