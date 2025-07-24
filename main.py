import os
import requests
from dotenv import load_dotenv
import streamlit as st
import time
from openai import AzureOpenAI


load_dotenv()
API_KEY = os.getenv("AZURE_API_KEY")
ENDPOINT = os.getenv("AZURE_API_ENDPOINT")
# Setting headers for the request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

st.set_page_config(page_title="Digitor for Korpa", layout="wide")

# Add a fixed header that stays visible when scrolling, with black background
st.markdown(
    """
    <style>
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        z-index: 1000;
        background-color: ; /* Black background */
        padding: 20px;
        border-radius: 0 0 10px 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .fixed-header h2, .fixed-header p {
        color: #FFFFFF;
    }
    .stApp {
        padding-top: 90px;
        background-color: #000000 !important;
    }
    </style>
    <div class='fixed-header'>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center;'>BMRI AI DIGITOR for Korpa</h1>", unsafe_allow_html=True)

chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = [] 

def get_chatbot_response(user_message, chat_history):
    # Prepare chat history for the request
    
    print("Chat History:", chat_history)  # For debugging purposes
    # Create the payload for the request
    payload = {
        "chat_input": user_message,
        "chat_history": chat_history,
    }


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


if chat_in := st.chat_input("Ketik pertanyaan atau permintaan Anda"):
    start_time = time.time()
    st.session_state.messages.append({"role": "user", "content": chat_in})

    # Get the response from the chatbot
    bot_response = get_chatbot_response(chat_in, chat_history)
    print("Bot Response:", bot_response)
    end_time = time.time()
    execution_time = end_time - start_time
    dataCompareModel = f"| Token {len(bot_response)} | {execution_time:.2f} detik"

    print("Resonponse Content:", bot_response)
    
    print(f"Execution time: {execution_time} seconds")
    bot_response = f"{bot_response}"

    if bot_response:
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        chat_history.append({
            "inputs": {"chat_input": chat_in},
            "outputs": {"chat_output": bot_response}
        })

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])
