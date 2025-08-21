import speech_recognition as sr

from pydub import AudioSegment

# Convert MP3 to WAV (if needed)
mp3_file = "audiobook.mp3"
wav_file = "audiobook.wav"

AudioSegment.from_mp3(mp3_file).export(wav_file, format="wav")

# Initialize recognizer
recognizer = sr.Recognizer()

# Load audio file
with sr.AudioFile(wav_file) as source:
    audio_data = recognizer.record(source)  # Read the entire file

# Try recognizing speech
try:
    text = recognizer.recognize_google(audio_data)
    print("Extracted Text:", text)
except sr.UnknownValueError:
    print("Could not understand the audio")
except sr.RequestError as e:
    print("API Error:", e)
