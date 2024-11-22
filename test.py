from langchain_community.llms import Ollama
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties for the TTS engine (optional)
engine.setProperty("rate", 150)  # Speed percent (can go over 100)
engine.setProperty("volume", 0.9)  # Volume 0-1

# Welcome message
welcome_message = "Welcome Sir, how may I help you?"
print(welcome_message)
engine.say(welcome_message)
engine.runAndWait()

# Initialize the LLM
llm = Ollama(model="deepseek-coder")

while True:
    # Get the prompt from the user
    prompt = input("Enter your prompt: ")

    # Invoke the LLM to get a response
    response = llm.invoke(prompt)

    # Print the response
    print(response)

    # Speak out the response
    engine.say(response)
    engine.runAndWait()

    # Ask if the user has another question
    follow_up_message = "Do you have another question? Yes or No"
    engine.say(follow_up_message)
    engine.runAndWait()

    another_question = (
        input("Do you have another question? Yes or No: ").strip().lower()
    )

    if another_question != "yes":
        goodbye_message = "Goodbye Sir. Have a great day!"
        print(goodbye_message)
        engine.say(goodbye_message)
        engine.runAndWait()
        break
