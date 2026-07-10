import sounddevice as sd
import speech_recognition as sr
import numpy as np

class VoiceController:
    def __init__(self):
        self.recognizer = sr.Recognizer()

        sd.default.device = 3

    def listen(self):
        duration = 5
        sample_rate = 44100

        print("Say your column...")

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype=np.int16
        )

        sd.wait()

        audio = sr.AudioData(
            recording.tobytes(),
            sample_rate,
            2
        )

        try:
            text = self.recognizer.recognize_google(audio)
            print("You said:", text)

            return self.convert_to_column(text)

        except Exception as e:
            print("Speech error:", repr(e))
            return -1

    def convert_to_column(self, text):
        numbers = {
            "one":0,
            "two":1,
            "three":2,
            "four":3,
            "five":4,
            "six":5,
            "seven":6
        }

        text = text.lower()

        for word in numbers:
            if word in text:
                return numbers[word]
        return -1