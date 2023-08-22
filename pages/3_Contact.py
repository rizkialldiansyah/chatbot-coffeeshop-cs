import streamlit as st

# ===============SETUP===============
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.set_page_config(
    page_title="Contact",
    page_icon="👨‍💻"
)
st.markdown(hide_st_style, unsafe_allow_html=True)
# Judul atau Header
st.title("Get in Touch")
contact_form = """
<form action="https://formsubmit.co/rzzkalldi@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your reviews here"></textarea>
     <button type="submit">Send</button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)

# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")