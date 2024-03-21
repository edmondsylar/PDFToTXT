import os
import streamlit as st
import pandas as pd
from io import StringIO
import random
import time


# import the ai model function.
from Models.GroqAI import GroqAi

system_prompt="You are a super AI assistant that helps user's understand their information much better."

# initialize the model
groqAssistant = GroqAi(apiKey="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", system_prompt=system_prompt, user={"username":"Edmond Musiitwa"})

# Import the function we defined earlier
from Transformer import process_single_pdf, process_pdfs_in_directory

# Set the Streamlit app to open in full screen mode
st.set_page_config(layout="wide")

# check that messages is not already in the session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# check that Gemini_messages is not already in the session state
if "Gemini_messages" not in st.session_state:
    st.session_state.Gemini_messages = []


# function 
def ChatGroq():

    _temp_response = ''
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            aiRes = callAIAssistant(prompt)
            _temp_response = aiRes
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(_temp_response))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})


# function to call the AI assistant
def callAIAssistant(message):
    response = groqAssistant.Chat(message)
    return response



def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)



# create 2 tabs (Home, Processed Files)
tabs = ["Home", "Copilot"]
page = st.sidebar.radio('Navigation', tabs)

if page == "Home":
    col1, col2 = st.columns([4, 6])

    with col1:
        st.subheader('Upload a PDF file')
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            filename = uploaded_file.name

            # Write the bytes data to a file
            with open(f"PDFs/{filename}", "wb") as f:
                f.write(bytes_data)

    with col2:
        st.subheader('Operations')
        st.markdown("Handle Operations on the uploaded Files")

        st.markdown("""---""")

        col1, col2 = st.columns(2)

        with col1:
            if st.button('Transform'):
                # Now process this file
                msg = process_pdfs_in_directory('PDFs/')
                st.write(msg)

        with col2:
            if st.button('Embed'):
                # Embedding code goes here
                st.write("Embedding code goes here")
            

    # Display a list of uploaded files in the sidebar
    st.sidebar.header('Uploaded Files')
    search_term = st.sidebar.text_input('Search files')

    uploaded_files = os.listdir('PDFs')
    for file in uploaded_files:
        if search_term in file:
            st.sidebar.write(file)

    # Count the number of processed and broken files
    processed_files_count = len(os.listdir('ProcessedFiles'))
    broken_files_count = len(os.listdir('BrokenFiles'))

    # simple label
    st.sidebar.markdown("#### Processed Files")
    # Display the counts in the sidebar
    st.sidebar.markdown(f"**Transformed Files:** {processed_files_count}")
    st.sidebar.markdown(f"**Broken Files:** {broken_files_count}")

elif page == "Copilot":

    st.subheader('A.L.F.I.E (Beta)')
    st.markdown("**Artificial Lifeform Intelligent Entity**")

    if st.button('Embed All Text Files'):
        st.write('Embedding all text files...')

    st.markdown("""---""")
    # columns layout
    col1, col2 = st.columns([3, 7])

    # column 1 - display the processed files
    with col1:
        st.markdown("#### TXT Data")

        processed_files = os.listdir('TXTData')
        for file in processed_files:
            st.write(file)

    
    # column 2 - display the content of the selected file
    with col2:
        st.markdown("### Copilot")
        
        # 
        Groq, Gemini = st.tabs(['Groq', 'Gemini'])
        
        with Groq:
            st.markdown('###### Groq AI')
            st.markdown('Powered  By ```Groq ```')

            # Chat with Groq
            ChatGroq()

        with Gemini:
            st.markdown('###### Gemini AI')
            st.markdown('Powered  By ```@googleDeepMind```')

        


