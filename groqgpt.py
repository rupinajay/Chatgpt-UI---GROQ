import streamlit as st
import time
from groq import Groq

# Initialize Groq client with your API key
client = Groq(api_key="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")  # Replace with your actual API key

# Set page configuration
st.set_page_config(page_title="ChatGPT-like Interface", layout="wide", initial_sidebar_state="expanded")

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

def get_response(user_query):
    """Get a response from Groq's model with retry logic."""
    st.session_state.conversation_history.append({"role": "user", "content": user_query})
    conversation_history = st.session_state.conversation_history[-10:]
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                messages=conversation_history,
                model="Llama-3.1-70b-Versatile",
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )
            assistant_response = response.choices[0].message.content
            st.session_state.conversation_history.append({"role": "assistant", "content": assistant_response})
            return assistant_response
        except Exception as e:
            if "rate limit" in str(e).lower():
                wait_time = 2 ** attempt
                st.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                st.error(f"Error: {e}")
                return None

def display_message(role, content):
    """Display a chat message."""
    # Monochrome colors
    if st.get_option('theme.primaryColor') == "#FFFFFF":  # Check if the primary color is white (light mode)
        user_bg_color = "#d9d9d9"  # Light gray for user
        assistant_bg_color = "#bfbfbf"  # Medium gray for assistant
        text_color = "#000000"  # Black text for light mode
    else:
        user_bg_color = "#4d4d4d"  # Dark gray for user
        assistant_bg_color = "#7f7f7f"  # Lighter gray for assistant
        text_color = "#ffffff"  # White text for dark mode

    if role == "user":
        st.markdown(f"""
        <div style="background-color: {user_bg_color}; padding: 10px; border-radius: 15px; text-align: right; margin-bottom: 10px; display: inline-block; color: {text_color}; float: right;">
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color: {assistant_bg_color}; padding: 10px; border-radius: 15px; margin-bottom: 10px; display: inline-block; color: {text_color}; float: left;">
            {content}
        </div>
        """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("ChatGPT")
    st.markdown("---")
    st.subheader("Conversations")
    st.text("Your conversations will appear here")

# Main chat interface
st.title("ChatGPT-like Interface")

# Display chat messages
for message in st.session_state.conversation_history:
    display_message(message["role"], message["content"])

# User input
user_input = st.text_area("Type your message here...", key="user_input", height=100, placeholder="Type your message here...", label_visibility="collapsed")
if user_input:
    response = get_response(user_input)

# Run the app
if __name__ == "__main__":
    pass  # No need for rerun here