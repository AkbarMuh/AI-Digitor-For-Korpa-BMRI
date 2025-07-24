import requests
import json
import os
from dotenv import load_dotenv

# Configuration and API Endpoint

load_dotenv()
API_KEY = os.getenv("AZURE_API_KEY")
ENDPOINT = os.getenv("AZURE_API_ENDPOINT")
# Setting headers for the request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

chat_history = []

# Sample user message and chat history
def get_chatbot_response(user_message, chat_history):
    # Prepare chat history for the request
    
    print("Chat History:", chat_history)  # For debugging purposes
    # Create the payload for the request
    payload = {
        "chat_input": user_message,
        "chat_history": chat_history,
    }

    #print("Payload:", payload)  # For debugging purposes

    # Send the request to Azure API
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            # Get the chat output from the response JSON
            return response_data.get("chat_output", "No response in JSON.")
        else:
            return f"Failed to reach the endpoint. Status code: {response.status_code}, Error: {response.text}"
    
    except requests.RequestException as e:
        return f"An error occurred: {e}"

# Function to simulate chat loop and get the response from chatbot
def chat_loop():
    chat_history = []  # Initialize empty chat history
    print("Chat started. Type 'exit' to end the conversation.")
    
    while True:
        # Get user input
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Ending chat session.")
            break

        # Send the message to the Azure API and get a response
        response = get_chatbot_response(user_input, chat_history)

        # Append the user input and assistant's response to chat history
        chat_history.append({
            "inputs": {"chat_input": user_input},
            "outputs": {"chat_output": response}
        })

        print(f"Assistant: {response}")

# Start the chat loop
chat_loop()
