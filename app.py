import speech_recognition as sr
import pyttsx3
import openai
from datetime import datetime
import random

USE_OPENAI_API = False  # Set to True to use api key
OPENAI_API_KEY = ""  # Put your key here if using OpenAI
openai.api_key = OPENAI_API_KEY if USE_OPENAI_API else None
EXIT_PHRASES = ["bye", "goodbye", "exit", "stop"]


# Setup text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()

# Offline response
def get_fallback_response(prompt):
    prompt = prompt.lower()
    if "hi" in prompt or "hello" in prompt:
        return "Hello! I am Chatterbox! How may I assist you today?"
    elif "your name" in prompt:
        return "I'm your voice assistant, My name is Chatterbox!"
    elif "how are you" in prompt:
        return "I'm doing great. How about you?"
    elif "time" in prompt:
        return f"The time now is {datetime.now().strftime('%I:%M %p')}."
    elif "date" in prompt:
        return f"Today's date is {datetime.now().strftime('%B %d, %Y')}."
    elif "joke" in prompt:
        return random.choice([
            "Why did the developer go broke? Because he used up all his cache!",
            "Why do Java developers wear glasses? Because they don’t C#!",
            "Why don’t programmers like nature? It has too many bugs."
        ])
    elif "what can you do" in prompt:
        return "I can answer your questions, tell you the time and date, and chat with you!"
    elif "how may i help you" in prompt:
        return "You can ask me anything, and I'll try to assist you!"
    else:
        return "I'm not sure about that, but I'm here to help!"

# Get response
def get_ai_response(prompt):
    if USE_OPENAI_API and OPENAI_API_KEY:
        try:
            print("Thinking...")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful voice assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"OpenAI Error: {str(e)}"
    else:
        return get_fallback_response(prompt)

# Recognize voice
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            print("📝 Recognizing...")
            text = recognizer.recognize_google(audio)
            print("You:", text)
            return text
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except Exception as e:
            print("Error:", str(e))
    return None

# Encouraging quotes after conversation ends
def get_encouraging_quote():
    return random.choice([
        "Keep pushing forward, success is just around the corner!",
        "Believe in yourself! You're capable of achieving great things.",
        "The best way to predict your future is to create it.",
        "Every day is a new opportunity to grow and improve!"
    ])

# Main loop
def main():
    print("Chatterbox : AI Assistant")
    print("Say something or 'bye' to quit.\n")
 
    
    while True:
        user_input = listen()
        if user_input:
            if any(exit_word in user_input.lower() for exit_word in EXIT_PHRASES):
                speak("Goodbye! Have a Nice Day!")
                speak(get_encouraging_quote())
                break
            response = get_ai_response(user_input)
            speak(response)

if __name__ == "__main__":
    main()
