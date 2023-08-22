import streamlit as st

# 
from drink_recommendation import DrinkRecommendationSystem
from chatbot_id import McobotChatbot
from chatbot_en import McobotChatbot_en

# ===============SETUP===============
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.set_page_config(
    page_title="Demo Chatbot",
    page_icon="👨‍💻"
)
st.markdown(hide_st_style, unsafe_allow_html=True)
# Configurasi

# Main App
st.title("M Coffee Company Chatbot")

# ===============CHATBOT SYSTTEM===============
# Language selection dropdown
language = st.selectbox("Select Language:", ["Indonesia", "English"])

# Recommendation System
menu_minuman_path = "data/rs/menu_miuman.csv"
RSystem = DrinkRecommendationSystem(menu_minuman_path)
# Responses Chabot
response_id = McobotChatbot() # class response indonesia language
response_en = McobotChatbot_en() # class response indonesia language
bahasa = "id" # default language

# Check if language has changed, reset conversation if true
if st.session_state.get("selected_language") != language:
    st.session_state.messages = []
    st.session_state.selected_language = language

# display msg to chatbot system
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# input msg
if prompt:= st.chat_input("Ketik pesan.."):
    # msg user
    with st.chat_message("user"):
        st.markdown(prompt)
    # add to history msg
    st.session_state.messages.append({"role": "user", "content": prompt})

    # msg chatbot
    with st.chat_message("mcobot"):
        response = ""
        if "/recommend" in prompt:
            if language == "Indonesia":
                response = RSystem.response_br(prompt)
            else:
                response = RSystem.response_br_en(prompt)
        else:
            if language == "Indonesia":
                response = f"Mcobot: {response_id.get_response(prompt)}"
            else:
                response = f"Mcobot: {response_en.get_response(prompt)}"
        st.markdown(response)
    st.session_state.messages.append({"role": "mcobot", "content": response})
