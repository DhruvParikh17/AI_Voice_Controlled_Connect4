import sounddevice as sd
import speech_recognition as sr
import numpy as np


class VoiceController:

    def __init__(self):
        #Initializes speech recognition tool used to process audio files into text
        self.recognizer = sr.Recognizer()

    def listen(self):
        #Records 5 seconds of microphone audio, sends it to Google Speech Recognition, and returns a column number.
        duration = 5
        sample_rate = 44100  # Standard high-quality audio sample rate

        print("Say your column...")

        try:
            # Step 1: Record audio from the microphone as numbers
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,  # Mono audio
                dtype=np.int16  # 16-bit PCM audio format
            )
            sd.wait()  # Wait until the 5 second recording is finished

            # Step 2: Convert the recorded audio into a format the speech recognizer can read
            audio = sr.AudioData(
                recording.tobytes(),
                sample_rate,
                2  # Sample width in bytes for 16-bit audio
            )

            # Step 3: Use Googles speech to text API to transcribe the audio recording into text
            text = self.recognizer.recognize_google(audio)
            print("You said:", text)

            # Step 4: Convert the transcribed text words into a board column index (0-6)
            return self.convert_to_column(text)

        except sr.UnknownValueError:
            # Error if speech was unclear
            print("Speech error: Could not understand audio")
            return -1
        except Exception as e:
            # Error if a connection error occurs
            print("Speech error:", repr(e))
            return -1

    def convert_to_column(self, text):
        # Converts spoken number words into corresponding grid column indexes
        numbers = {
            "one": 0,
            "two": 1,
            "three": 2,
            "four": 3,
            "five": 4,
            "six": 5,
            "seven": 6
        }

        text = text.lower()  # Convert speech text to lowercase

        # Check if any number word appears in what the user said
        for word in numbers:
            if word in text:
                return numbers[word]

        return -1  # If no valid column word was recognized