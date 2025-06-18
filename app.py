import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
import time
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Welcome to M³ - Mani's Money Matters Personal Finance Guide",
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
    .calculator-result {
        background-color: #e8f5e8;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
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
    st.header("💰 M³ - Your Personal Finance Guide")
    
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
    
    # FINANCIAL CALCULATORS SECTION
    st.header("🧮 Financial Calculators")
    
    # Calculator selection
    calculator_type = st.selectbox(
        "Choose Calculator:",
        ["Select Calculator", "SIP Calculator", "Compound Interest", "Loan EMI", "FD Calculator", "PPF Calculator"]
    )
    
    # SIP Calculator
    if calculator_type == "SIP Calculator":
        st.subheader("📈 SIP Calculator")
        sip_amount = st.number_input("Monthly SIP Amount (₹)", min_value=500, value=5000, step=500)
        sip_rate = st.number_input("Expected Annual Return (%)", min_value=1.0, value=12.0, step=0.5)
        sip_years = st.number_input("Investment Period (Years)", min_value=1, value=10, step=1)
        
        if st.button("Calculate SIP", key="sip_calc"):
            monthly_rate = sip_rate / 100 / 12
            months = sip_years * 12
            future_value = sip_amount * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
            total_invested = sip_amount * months
            gains = future_value - total_invested
            
            st.markdown(f"""
            <div class="calculator-result">
                <strong>💰 Results:</strong><br>
                Total Invested: ₹{total_invested:,.0f}<br>
                Maturity Amount: ₹{future_value:,.0f}<br>
                Wealth Gain: ₹{gains:,.0f}
            </div>
            """, unsafe_allow_html=True)
    
    # Compound Interest Calculator
    elif calculator_type == "Compound Interest":
        st.subheader("💰 Compound Interest")
        principal = st.number_input("Principal Amount (₹)", min_value=1000, value=100000, step=1000)
        ci_rate = st.number_input("Annual Interest Rate (%)", min_value=1.0, value=8.0, step=0.5)
        ci_years = st.number_input("Time Period (Years)", min_value=1, value=5, step=1)
        compound_freq = st.selectbox("Compounding", ["Annually", "Half-yearly", "Quarterly", "Monthly"])
        
        if st.button("Calculate Compound Interest", key="ci_calc"):
            freq_map = {"Annually": 1, "Half-yearly": 2, "Quarterly": 4, "Monthly": 12}
            n = freq_map[compound_freq]
            amount = principal * (1 + (ci_rate/100)/n)**(n*ci_years)
            interest = amount - principal
            
            st.markdown(f"""
            <div class="calculator-result">
                <strong>💰 Results:</strong><br>
                Principal: ₹{principal:,.0f}<br>
                Maturity Amount: ₹{amount:,.0f}<br>
                Interest Earned: ₹{interest:,.0f}
            </div>
            """, unsafe_allow_html=True)
    
    # Loan EMI Calculator
    elif calculator_type == "Loan EMI":
        st.subheader("🏠 Loan EMI Calculator")
        loan_amount = st.number_input("Loan Amount (₹)", min_value=50000, value=1000000, step=50000)
        loan_rate = st.number_input("Interest Rate (% per annum)", min_value=1.0, value=9.5, step=0.25)
        loan_tenure = st.number_input("Loan Tenure (Years)", min_value=1, value=20, step=1)
        
        if st.button("Calculate EMI", key="emi_calc"):
            monthly_rate = loan_rate / 100 / 12
            months = loan_tenure * 12
            emi = loan_amount * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
            total_amount = emi * months
            total_interest = total_amount - loan_amount
            
            st.markdown(f"""
            <div class="calculator-result">
                <strong>💰 Results:</strong><br>
                Monthly EMI: ₹{emi:,.0f}<br>
                Total Amount: ₹{total_amount:,.0f}<br>
                Total Interest: ₹{total_interest:,.0f}
            </div>
            """, unsafe_allow_html=True)
    
    # FD Calculator
    elif calculator_type == "FD Calculator":
        st.subheader("🏦 Fixed Deposit Calculator")
        fd_amount = st.number_input("FD Amount (₹)", min_value=1000, value=100000, step=1000)
        fd_rate = st.number_input("Interest Rate (% per annum)", min_value=1.0, value=6.5, step=0.25)
        fd_years = st.number_input("FD Tenure (Years)", min_value=1, value=3, step=1)
        
        if st.button("Calculate FD", key="fd_calc"):
            maturity_amount = fd_amount * (1 + fd_rate/100)**fd_years
            interest_earned = maturity_amount - fd_amount
            
            st.markdown(f"""
            <div class="calculator-result">
                <strong>💰 Results:</strong><br>
                Principal: ₹{fd_amount:,.0f}<br>
                Maturity Amount: ₹{maturity_amount:,.0f}<br>
                Interest Earned: ₹{interest_earned:,.0f}
            </div>
            """, unsafe_allow_html=True)
    
    # PPF Calculator
    elif calculator_type == "PPF Calculator":
        st.subheader("🏛️ PPF Calculator")
        ppf_annual = st.number_input("Annual PPF Amount (₹)", min_value=500, value=150000, step=500, help="Max: ₹1.5 lakh per year")
        ppf_years = st.selectbox("PPF Tenure", [15, 20, 25, 30], index=0)
        ppf_rate = st.number_input("PPF Interest Rate (%)", min_value=7.0, value=7.1, step=0.1, help="Current rate: 7.1%")
        
        if st.button("Calculate PPF", key="ppf_calc"):
            # PPF calculation with annual compounding
            maturity_amount = ppf_annual * (((1 + ppf_rate/100)**ppf_years - 1) / (ppf_rate/100))
            total_invested = ppf_annual * ppf_years
            tax_free_gains = maturity_amount - total_invested
            
            st.markdown(f"""
            <div class="calculator-result">
                <strong>💰 Results:</strong><br>
                Total Invested: ₹{total_invested:,.0f}<br>
                Maturity Amount: ₹{maturity_amount:,.0f}<br>
                Tax-free Gains: ₹{tax_free_gains:,.0f}
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Model settings
    model_name = "gemini-1.5-flash"
    temperature = 0.7
       
    # Instructions
    st.header("📋 How to Use")
    st.markdown("""
    **Financial Calculators**: Use the calculators above for quick calculations!
    
    **Chat with M³**: Ask any personal finance question!
    
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
    <h1>💰 M³ (Mani's Money Matters Guide) </h1>
    <h3>Your Personal Finance Guide</h3>
    <p>Friendly advice on investments, savings, insurance, and financial planning</p>
</div>
""", unsafe_allow_html=True)

# System prompt - customize this with your AI Studio instructions
SYSTEM_PROMPT = """You are "M³ (Mani's Money Matters Guide)," a knowledgeable and friendly personal finance guide from India. Your role is to help users with:

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
- Say Hello instead of Namaste

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
                with st.spinner("M³ is thinking..."):
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
