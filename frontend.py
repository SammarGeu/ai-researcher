

import streamlit as st
from ai_researcher_2 import INITIAL_PROMPT, graph, get_session_config
from pathlib import Path
import logging
from langchain_core.messages import AIMessage
import uuid
import re # Import regular expressions

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Basic app config
st.set_page_config(page_title="Research AI Agent", page_icon="📄")
st.title("📄 Research AI Agent")
                             
                             
# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.info("Initialized chat history")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    logger.info(f"Initialized new session_id: {st.session_state.session_id}")

# --- Helper function to find PDF path and show button ---
def display_pdf_downloader(content: str):
    """Parses content for a PDF path and displays a download button if found."""
    # Regex to find an absolute path in backticks, e.g., `.../output/paper_...pdf`
    # This matches the "Path: `...`" string returned by write_pdf.py
    match = re.search(r"`(/[^`]+\.pdf)`", content)
    if match:
        pdf_path_str = match.group(1)
        pdf_path = Path(pdf_path_str)
        
        if pdf_path.exists():
            try:
                # Read the file data
                with open(pdf_path, "rb") as f:
                    file_data = f.read()
                
                # Create the download button
                st.download_button(
                    label=f"Download {pdf_path.name}",
                    data=file_data,
                    file_name=pdf_path.name,
                    mime="application/pdf",
                    # Add a unique key to prevent streamlit errors
                    key=f"download_{pdf_path.name}_{uuid.uuid4()}" 
                )
            except Exception as e:
                logger.error(f"Failed to create download button for {pdf_path}: {e}")
                st.error(f"Could not read file: {pdf_path.name}")
        else:
            # This can happen if the file was deleted
            logger.warning(f"AI mentioned PDF '{pdf_path_str}' but it does not exist.")


# --- Chat History Display ---
# Display all past messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # --- NEW: Check for download button on history ---
        # This makes the button "stick" even after reloading
        if msg["role"] == "assistant":
            display_pdf_downloader(msg["content"])


# --- Chat Input and Agent Logic ---
user_input = st.chat_input("What research topic would you like to explore?")

if user_input:
    logger.info(f"User input: {user_input}")
    
    # Add user message to history and display it
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare the input for the LangGraph agent
    chat_input = {
        "messages": [{"role": "system", "content": INITIAL_PROMPT}] + st.session_state.chat_history
    }
    
    # Get the unique session config
    session_config = get_session_config(st.session_state)
    logger.info(f"Starting agent processing for session: {session_config['configurable']['thread_id']}")

    full_response_text = ""
    
    # Display the assistant's response in a chat message
    with st.chat_message("assistant"):
        response_placeholder = st.empty() # Placeholder for streaming text

        # Stream the response from the graph
        for chunk in graph.stream(chat_input, session_config, stream_mode="values"):
            
            message = chunk["messages"][-1]
            
            # Log any tool calls
            if getattr(message, "tool_calls", None):
                for tool_call in message.tool_calls:
                    logger.info(f"Tool call: {tool_call['name']}")
            
            # Check if the message is from the AI and has content
            if isinstance(message, AIMessage) and message.content:
                text_chunk = ""
                
                # --- THIS IS THE FIX FOR YOUR ORIGINAL "GARBLED TEXT" PROBLEM ---
                if isinstance(message.content, list):
                    # Handle complex content (e.g., [{'type': 'text', 'text': '...'}])
                    for part in message.content:
                        if isinstance(part, dict) and part.get('type') == 'text':
                            text_chunk += part.get('text', '')
                        elif isinstance(part, str):
                            text_chunk += part
                
                elif isinstance(message.content, str):
                    # Handle simple string content
                    text_chunk = message.content
                
                if text_chunk:
                    # This logic handles streaming values vs. full updates
                    if text_chunk.startswith(full_response_text):
                        # Append new text (streaming)
                        new_text = text_chunk[len(full_response_text):]
                        full_response_text += new_text
                        response_placeholder.markdown(full_response_text + "▌")
                    else: 
                        # Replace text (non-streaming, like after a tool call)
                        full_response_text = text_chunk
                        response_placeholder.markdown(full_response_text + "▌")

        # Final update without the typing cursor
        response_placeholder.markdown(full_response_text)

    # Add the final, complete response to history
    if full_response_text:
        st.session_state.chat_history.append({"role": "assistant", "content": full_response_text})
        logger.info(f"Full response added to history.")

        # --- NEW FEATURE: ADD DOWNLOAD BUTTON ---
        # Check if the final response contains a PDF path and show the button
        display_pdf_downloader(full_response_text)

