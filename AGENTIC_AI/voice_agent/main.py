import speech_recognition as sr
from google import genai
from dotenv import load_dotenv
import os
import pyttsx3


load_dotenv()
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"] 
AI_MODEL = os.environ["GOOGLE_GEMINI_MODEL"] 
client = genai.Client(api_key=GEMINI_API_KEY)

def speech_to_text():
    r = sr.Recognizer() # Speech to Text
     
    with sr.Microphone() as source: # Mic Access
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2
        
        print("Speak Something...")
        audio = r.listen(source)
        # print(sr.Microphone.list_microphone_names())  # list microphone 
        print("Processing Audion.. (STT)")
        stt = r.recognize_google(audio)
         
        print("You said...\n",stt)  
        
        full_prompt = f""" 
        You are an expert voice agent. You are given the transcript of what user has said  using voice.
        You nee to output as if you are an voice agent and whatever you speek 
        will be converted back to audio using AI and played back to user
        
        "user_said": {stt}
        """
        ai_response = client.models.generate_content(
        model=AI_MODEL,
        contents=full_prompt )
        
        print(ai_response.text)
        
        return ai_response.text
     
stt = speech_to_text()  

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

text_to_speech(stt)

    