import speech_recognition as sr
import cv2
import os

print(sr.Microphone.list_microphone_names())

import speech_recognition as sr

recognizer = sr.Recognizer()

# List all available microphones
#print("Available microphones:")
#for index, name in enumerate(sr.Microphone.list_microphone_names()):
#    print(f"{index}: {name}")

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Please say something:")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")


def play_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def load_video_files_from_folder(folder_path):
    video_files = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4"):
            key = os.path.splitext(filename)[0].lower()
            video_files[key] = os.path.join(folder_path, filename)
    return video_files

def main():
    folder_path = "C:/Users/user/Desktop/python_project/avatar"  # Update this with the path to your folder
    video_files = load_video_files_from_folder(folder_path)

    if not video_files:
        print("No video files found in the folder.")
        return

    speech_text = speech_to_text()
    if speech_text:
        words = speech_text.split()
        for word in words:
            word = word.lower()
            if word in video_files:
                video_path = video_files[word]
                print(f"Playing video: {video_path}")
                play_video(video_path)
                break
        else:
            print("No matching video found.")

if _name_ == "_main_":
    main()