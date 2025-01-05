import logging
from langchain_community.llms import Ollama
import pyttsx3
import speech_recognition as sr
import configparser
import sys

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties for the TTS engine from configuration
engine.setProperty("rate", config.getint('TTS', 'rate', fallback=162))
engine.setProperty("volume", config.getfloat('TTS', 'volume', fallback=0.9))

# Initialize the LLM
llm = Ollama(model=config.get('LLM', 'model', fallback="deepseek-coder"))

# Initialize the recognizer
recognizer = sr.Recognizer()

def speak(text):
    """Speak the given text using TTS engine."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to the user's speech and return the recognized text."""
    with sr.Microphone() as source:
        logging.info("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        speak("I'm listening now. Please speak.")

        logging.info("Listening...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        try:
            prompt = recognizer.recognize_google(audio)
            logging.info(f"You said: {prompt}")
            return prompt
        except sr.UnknownValueError:
            logging.error("Could not understand the speech.")
            speak("Sorry, I could not understand your speech. Please try again.")
        except sr.RequestError as e:
            logging.error(f"Could not request results; {e}")
            speak("There seems to be an issue with the connection. Please check your internet.")
        except sr.WaitTimeoutError:
            logging.error("No speech detected.")
            speak("I couldn't hear anything. Please try speaking again.")
        return None

def main():
    """Main function to run the assistant."""
    welcome_message = "Welcome Spectre, how may I help you?"
    logging.info(welcome_message)
    speak(welcome_message)

    while True:
        input_mode_message = "Would you like to type your prompt or speak to me? Enter 'type' or 'speak'."
        logging.info(input_mode_message)
        speak(input_mode_message)

        input_mode = input("Enter 'type' or 'speak': ").strip().lower()

        if input_mode == "type":
            prompt = input("Enter your prompt: ")
        elif input_mode == "speak":
            prompt = listen()
            if not prompt:
                continue
        else:
            invalid_input_message = "Invalid input. Please enter 'type' or 'speak'."
            logging.warning(invalid_input_message)
            speak(invalid_input_message)
            continue

        # Invoke the LLM to get a response
        logging.info("Processing your request...")
        response = llm.invoke(prompt)

        # Print and speak the response
        logging.info(response)
        speak(response)

        # Ask if the user has another question
        follow_up_message = "Do you have another question? Please say 'yes' or 'no'."
        logging.info(follow_up_message)
        speak(follow_up_message)

        another_question = input("Do you have another question? Yes or No: ").strip().lower()

        if another_question not in ["yes", "y"]:
            goodbye_message = "Goodbye Spectre. Have a great day!"
            logging.info(goodbye_message)
            speak(goodbye_message)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Exiting gracefully.")
        sys.exit(0)
