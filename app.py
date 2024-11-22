from langchain_community.llms import Ollama
import pyttsx3
import speech_recognition as sr

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties for the TTS engine
engine.setProperty("rate", 162)  # Speed percent (can go over 100)
engine.setProperty("volume", 0.9)  # Volume 0-1

# Initialize the LLM
llm = Ollama(model="deepseek-coder")

# Initialize the recognizer
recognizer = sr.Recognizer()

# Welcome message
welcome_message = "Welcome Spectre, how may I help you, Sir?"
print(welcome_message)
engine.say(welcome_message)
engine.runAndWait()

while True:
    # Ask whether to enter the prompt or speak through the mic
    input_mode_message = (
        "Would you like to type your prompt or speak to me? Enter 'type' or 'speak'."
    )
    print(input_mode_message)
    engine.say(input_mode_message)
    engine.runAndWait()

    input_mode = input("Enter 'type' or 'speak': ").strip().lower()

    if input_mode == "type":
        prompt = input("Enter your prompt: ")
    elif input_mode == "speak":
        try:
            with sr.Microphone() as source:
                print("Adjusting for ambient noise... Please wait.")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                engine.say("I'm listening now. Please speak.")
                engine.runAndWait()

                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                prompt = recognizer.recognize_google(audio)
                print(f"You said: {prompt}")
        except sr.UnknownValueError:
            print("Sorry, I could not understand your speech.")
            engine.say("Sorry, I could not understand your speech. Please try again.")
            engine.runAndWait()
            continue
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(
                "There seems to be an issue with the connection. Please check your internet."
            )
            engine.runAndWait()
            continue
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            engine.say("I couldn't hear anything. Please try speaking again.")
            engine.runAndWait()
            continue
    else:
        invalid_input_message = "Invalid input. Please enter 'type' or 'speak'."
        print(invalid_input_message)
        engine.say(invalid_input_message)
        engine.runAndWait()
        continue

    # Invoke the LLM to get a response
    print("Processing your request...")
    response = llm.invoke(prompt)

    # Print and speak the response
    print(response)
    engine.say(response)
    engine.runAndWait()

    # Ask if the user has another question
    follow_up_message = "Do you have another question? Please say 'yes' or 'no'."
    print(follow_up_message)
    engine.say(follow_up_message)
    engine.runAndWait()

    another_question = input("Do you have another question? Yes or No: ").strip().lower()

    if another_question not in ["yes", "y"]:
        goodbye_message = "Goodbye Spectre. Have a great day, Sir!"
        print(goodbye_message)
        engine.say(goodbye_message)
        engine.runAndWait()
        break
