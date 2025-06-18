import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Welcome to M³ (Make Money with Mani) - Your Personal Finance Guide",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #1f4e79, #2e6da4);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #2e6da4;
    }
    .user-message {
        background-color: #f0f7ff;
        border-left-color: #2e6da4;
    }
    .assistant-message {
        background-color: #f8f9fa;
        border-left-color: #28a745;
    }
    .sidebar .element-container {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False

# Sidebar for API key and settings
with st.sidebar:
    st.header("💰 M³ (Make Money with Mani) - Your Personal Finance Guide")
    
    # API Key input
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        st.session_state.api_key_set = True
    else:
        api_key = st.text_input(
            "Enter your Gemini API Key:",
            type="password",
            help="Get your free API key from https://makersuite.google.com/app/apikey"
        )
        if api_key:
            genai.configure(api_key=api_key)
            st.session_state.api_key_set = True
    
    st.divider()
    
    # Model settings
    model_name = "gemini-1.5-flash"
    temperature = 0.7
       
    # Instructions
    st.header("📋 How to Use")
    st.markdown("""
    **Start Chatting**: Ask any personal finance question!
    
    **Example Questions:**
    - How should I plan my retirement?
    - What's the best investment strategy for beginners?
    - How to create an emergency fund?
    - Should I pay off debt or invest?
    """)

    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    
# Main header
st.markdown("""
<div class="main-header">
    <h1>💰 M³ (Make Money with Mani) </h1>
    <h3>Your Personal Finance Guide</h3>
    <p>Friendly advice on investments, savings, insurance, and financial planning</p>
</div>
""", unsafe_allow_html=True)

# System prompt - customize this with your AI Studio instructions
SYSTEM_PROMPT = """You are "M³ (Make Money with Mani)," a knowledgeable and friendly personal finance guide from India. Your role is to help users with:

• Investment planning (mutual funds, stocks, bonds, PPF, ELSS)
• Retirement planning and pension schemes
• Insurance (life, health, term insurance)
• Tax planning and savings under 80C, 80D
• Emergency fund creation
• Debt management and loan advice
• Real estate investment guidance
• Financial goal setting and budgeting

Your personality:
- Warm, friendly, and approachable like a trusted family elder
- Use simple, practical language that anyone can understand
- Give specific, actionable advice with examples
- Always consider the Indian financial landscape and regulations
- Emphasize long-term wealth building over quick gains
- Be conservative and risk-aware in your recommendations

Always provide practical, actionable advice relevant to Indian financial markets, tax laws, and investment options. Use simple language and give examples when possible. If you're unsure about specific current rates or regulations, advise the user to verify with current sources. Always ask clarifying questions when needed and provide step-by-step guidance. Use real Indian examples and current market context when possible.

Key guidelines:
- Always ask about the user's age, income level, and risk tolerance before giving investment advice
- Mention specific Indian investment options like ELSS, PPF, NSC, etc.
- Always remind users about the importance of emergency funds
- Suggest starting with SIPs for beginners
- Do not provide direct stock recommendations
- Always mention consulting with a financial advisor for decisions

Respond in a friendly manner as if you're a trusted family advisor.

Be encouraging and supportive while being realistic about financial goals."""

# Check if API key is set
if not st.session_state.api_key_set:
    st.warning("👈 Please enter your Gemini API key in the sidebar to start chatting!")
    st.info("""
    **Quick Start:**
    1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Sign in with your Google account
    3. Click "Create API Key"
    4. Copy and paste it in the sidebar
    5. Start asking financial questions!
    """)
else:
    # Initialize the model
    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=2048,
            ),
            system_instruction=SYSTEM_PROMPT
        )
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about personal finance..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate assistant response
            with st.chat_message("assistant"):
                with st.spinner("Mcube is thinking..."):
                    try:
                        # Create chat session for context
                        chat_history = []
                        for msg in st.session_state.messages[:-1]:  # Exclude the current message
                            if msg["role"] == "user":
                                chat_history.append({"role": "user", "parts": [msg["content"]]})
                            else:
                                chat_history.append({"role": "model", "parts": [msg["content"]]})
                        
                        # Start chat session
                        chat = model.start_chat(history=chat_history)
                        
                        # Get response
                        response = chat.send_message(prompt)
                        response_text = response.text
                        
                        # Display response
                        st.markdown(response_text)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                        
                    except Exception as e:
                        st.error(f"Error generating response: {e}")
                        st.info("Please check your API key and try again.")
    
    except Exception as e:
        st.error(f"Error initializing model: {e}")
        st.info("Please check your API key and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>💡 <strong>Disclaimer:</strong> This is for educational purposes. Always consult with qualified financial advisors for major decisions.</p>
</div>
""", unsafe_allow_html=True)
