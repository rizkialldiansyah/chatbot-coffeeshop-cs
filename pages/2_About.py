import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from drink_recommendation import DrinkRecommendationSystem
from explainer import LimeExplainer
import matplotlib.pyplot as plt
from util.input_prep import text_cleansing, slang_processing, stemming, remove_stopwords
from chatbot_id import McobotChatbot
import toml

menu_minuman_path = "data/rs/menu_miuman.csv"
RSystem = DrinkRecommendationSystem(menu_minuman_path)
explainer_id = LimeExplainer("./var/data_var_id.pth")
st.set_option('deprecation.showPyplotGlobalUse', False)
padding = McobotChatbot()
class_names = explainer_id.class_names

# ===============SETUP===============
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.set_page_config(
    page_title="About Chatbot",
    page_icon="👨‍💻",
    layout="wide"
)
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("About The Chatbot System")
selected_side = option_menu(
    menu_title = None,
    options=["About Mcobot", "Interpretation", "Recommendation System"],
    icons=["robot", "body-text", "diagram-3"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)
config_path = "./.streamlit/config.toml"
config = toml.load(config_path)
primary_color = config['theme']['primaryColor']
background_color = config['theme']['backgroundColor']
secondary_background_color = config['theme']['secondaryBackgroundColor']
text_color = config['theme']['textColor']
font = config['theme']['font']
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b

def create_colored_html(results):
    html = ""
    for word, prob in results:
        brightness = int(prob * 255)
        font_color = "black" if brightness > 143 else "white"
        background_color = f"rgb({0}, {brightness}, {0})"
        if prob > 0.9:
            background_color = "rgb(108, 68, 29)"
        font_style = f"font-family: sans-serif; font-size: 14px; font-weight: 800; color: {font_color}; padding: 3px 5px;"
        html += f'<span style="background-color:{background_color}; {font_style}">{word}</span> '
    return html
#======================ABOUT MCOBOT======================
if selected_side == "About Mcobot":
    with st.container():
        st.header("What is Mcobot?")
        st.write("##")
        st.write("""
                Mcobot adalah chatbot relative-based yang dikembangkan oleh Rizki Aldiansyah, dirancang khusus untuk M Coffee Company, sebuah kedai kopi yang terletak di Bandung. Chatbot ini memiliki kemampuan untuk memahami konteks dari pertanyaan pengguna, baik dalam Bahasa Indonesia maupun Bahasa Inggris.\n
                Chatbot ini menggunakan kombinasi algoritma Word2Vec dan LSTM untuk mengklasifikasikan pertanyaan pengguna. Selain itu, Mcobot juga mampu memberikan rekomendasi minuman kepada pengguna dengan mencocokkan preferensi pengguna dengan preferensi menu minuman yang tersedia.\n
                Dalam memberikan rekomendasi, Mcobot menggunakan metode Content-Based Filtering dengan menggunakan algoritma cosine similarity. Hal ini memungkinkan chatbot untuk menghitung tingkat kesamaan antara preferensi menu minuman dan preferensi pengguna, sehingga memberikan rekomendasi yang sesuai.\n
                Kami dengan senang hati mempersembahkan Mcobot sebagai asisten yang dapat membantu Anda menemukan minuman kopi yang cocok dengan selera Anda di M Coffee Company.\n
                """)
    #---About The Chatbot Model---
    with st.container():
        st.header("How Mcobot Works?")
        st.write("##")
        
        # Menampilkan Gif ditengah
        margl_img1, img1, margr_img1 = st.columns((1,4,1))
        with margl_img1:
            st.write(' ')
        with img1:
            st.image("./cache/flow_response.gif", use_column_width="auto",caption="Proses sistem dalam memproses pertanyaan hingga memberi respons")
        with margr_img1:
            st.write(' ')

        # Penjelasan mengenai Cara Kerja
        st.write("""
                 Seperti yang tergambar di atas, pertanyaan dari pengguna akan melalui serangkaian tahapan sebelum akhirnya mendapatkan respons yang kemungkinan besar sesuai dengan konteksnya. Proses ini terdiri dari langkah-langkah berikut:
                 1. **Pemrosesan Teks**: Pertanyaan yang diajukan oleh pengguna pertama-tama akan mengalami pemrosesan teks. Langkah ini mengubah dan memperbaiki pertanyaan dari pengguna agar sesuai dengan pemahaman model.
                 2. **Penyelarasan Panjang**: Pertanyaan yang telah diolah akan diubah menjadi sekumpulan token, yang kemudian akan disesuaikan panjangnya. Penyesuaian ini penting agar pertanyaan memiliki dimensi yang cocok dengan dimensi masukan model LSTM.
                 3. **Pembentukan Vektor**: Setelah penyelarasan panjang, pertanyaan akan diubah menjadi vektor. Proses ini menggunakan hasil pelatihan Word2Vec. Setiap kata dalam pertanyaan akan diubah menjadi vektor dengan makna yang terkait dengan kata-kata lainnya. Langkah ini membantu model untuk memahami konteks pertanyaan pengguna.
                 4. **Prediksi dengan Model LSTM**: Teks yang telah diubah menjadi vektor akan dimasukkan ke dalam model LSTM untuk dilakukan prediksi. Hasil dari prediksi ini berupa probabilitas untuk setiap label yang mungkin. Label dengan probabilitas tertinggi akan digunakan dalam langkah berikutnya.
                 5. **Pemilihan Respons**: Berdasarkan probabilitas, chatbot akan memilih label yang sesuai. Terdapat logika yang diterapkan dalam pemilihan label ini. Jika probabilitas kurang dari nilai yang ditentukan, chatbot akan merespons bahwa ia tidak mengerti konteks pertanyaan. Sebaliknya, jika probabilitas di atas nilai yang ditentukan, chatbot akan memberikan respons yang sesuai dengan label.
                 6. **Pemilihan Respons Acak**: Akhirnya, respons yang telah dipilih pada langkah sebelumnya akan dipilih secara acak dan dikirimkan kepada pengguna sebagai respons dari chatbot.                 
                 """)
    #---About The Recommendation System--
    with st.container():
        st.header("How Mcobot Suggests Drinks Based on User Preferences?")
        st.write("##")
        
        # Tampilkan file GIF dengan st.image()
        st.image("./cache/flow_rb.gif", use_column_width="auto",caption="Proses sistem dalam memberikan rekomendasi minuman")

        # Tampilkan teks atau konten lain di bawah GIF
        st.write("""
                 Seperti yang tergambar di atas, pertanyaan dari pengguna akan melalui serangkaian tahapan sebelum akhirnya mendapatkan respons yang sesuai dengan konteksnya. Proses ini terdiri dari langkah-langkah berikut:
                 1. **Ekstraksi Fitur**: Pertama-tama, preferensi pengguna diekstraksi dan diubah menjadi vektor nilai.
                 2. **Normalisasi Fitur (Standard Scaler)**: Vektor yang dihasilkan dari langkah sebelumnya dinormalisasi menggunakan rumus skala standar, sehingga nilai vektornya berada dalam rentang 0 hingga 1.
                 3. **Perhitungan Kemiripan Cosine**: Kami menghitung nilai kemiripan cosine antara preferensi pengguna dan preferensi yang terdapat pada menu.
                 4. **Perangkingan dan Pengambilan 3 Teratas**: Hasil perhitungan cosine similarity kemudian diurutkan dari yang terbesar hingga yang terkecil, dan kami memilih 3 menu teratas sebagai rekomendasi.
                 5. **Konversi Preferensi Menjadi Kalimat**: Akhirnya, preferensi dari ketiga menu teratas diubah menjadi kalimat yang akan dijadikan respons oleh chatbot.
                 """)
#======================INTERPRETATION MODEL======================
if selected_side == "Interpretation":
    st.header("Interpretation Model")
    st.write("Halaman ini akan menjelaskan bagaimana chatbot dapat memprediksi pertanyaan kedalam label. Anda dapat menginputkan text bahasa Indonesia pada bagian yang disediakan, lalu setelah anda menekan button proses, selanjutnya sistem akan otomatis memproses dan memberikan 4 label dengan probabilitas tertinggi. Adapun hasil-hasil saat dilakukan pemrosesan teks yang dapat anda lihat pada bagian setelah menginputkan teks")
    text = st.text_input("Input a text here")
    show_content = st.button("Tampilkan Konten Di Atas")

    #---Text Preprocessing---
    st.write("---")
    st.subheader("Text Preprocessing")
    with st.expander("***Original Text***"):
        st.write(text)
    text_clean = text_cleansing(text)
    with st.expander("***Text Cleansing***"):
        st.write(text_clean)
    slang_prep = slang_processing(text_clean)
    with st.expander("***Normalisasi Slang***"):
        st.write(slang_prep)
    stemmed = stemming(slang_prep)
    with st.expander("***Stemming***"):
        st.write(stemmed)
    removed = remove_stopwords(stemmed)
    with st.expander("***Remove Stopword***"):
        st.write(removed)
    padded = padding.text_prep(text)
    with st.expander("***Pad Sequence***"):
        st.write(padded)
    
    #---Explainer---
    if text == "":
        exp = explainer_id.explainer.explain_instance("default", explainer_id.predict_proba, top_labels=4)
        labels = exp.available_labels()
    else:
        exp = explainer_id.explainer.explain_instance(' '.join(removed), explainer_id.predict_proba, top_labels=4)
        labels = exp.available_labels()
    st.write("---")
    st.subheader("Model Explainer (Lime)")
    probabilities = exp.predict_proba
    st.info(f"***Model memprediksi label \"{class_names[labels[0]]}\" dengan tingkat kepercayaan sebesar {round(probabilities[labels[0]]*100, 2)}%***")
    st.write("Dalam contoh di bawah, menampilkan fitur-fitur penting yang mempengaruhi prediksi label. Semakin penting fitur, semakin hijau latar belakang kata tersebut.")
    components.html(create_colored_html((exp.as_list(label=labels[0]))),height=30)
    
    st.write("---")
    st.subheader("Visualizing Important Features from the Top 4 Tables")
    show_label_1 = True
    show_label_2 = False
    show_label_3 = False
    show_label_4 = False
    st.write(f"**Silakan Pilih Salah Satu dari Tiga Label dengan Probabilitas Tertinggi selain Label \"{class_names[labels[0]]}\" yang Telah Berhasil Diprediksi, untuk Ditampilkan Visualisasinya:** ")
    col1, col2, col3, col4 = st.columns(4)
    # Ganti variabel show_label_1 menjadi checkbox_label_1
    show_label_1 = col1.checkbox(f"{class_names[labels[0]]}", key="label_1",disabled=True,value=True)
    # Ganti variabel show_label_2 menjadi checkbox_label_2
    show_label_2 = col2.checkbox(f"{class_names[labels[1]]}", key="label_2",value=True)
    # Ganti variabel show_label_3 menjadi checkbox_label_3
    show_label_3 = col3.checkbox(f"{class_names[labels[2]]}", key="label_3")
    # Ganti variabel show_label_4 menjadi checkbox_label_4
    show_label_4 = col4.checkbox(f"{class_names[labels[3]]}", key="label_4")

    total_selected = show_label_1 + show_label_2 + show_label_3 + show_label_4


    selected_labels = []
    # Append atau remove label yang dipilih ke dalam list selected_labels
    for idx, label in enumerate(labels):
        if eval(f"show_label_{idx+1}"):
            if label not in selected_labels:
                selected_labels.append(label)
        else:
            if label in selected_labels:
                selected_labels.remove(label)

    if total_selected == 0:   
        selected_columns = st.columns(1)
    elif total_selected == 4:
        selected_columns_r1 = st.columns(2)
        selected_columns_r2 = st.columns(2)
    else:
        selected_columns = st.columns(total_selected)
    
    # Tampilkan teks di setiap kolom yang dipilih
    if total_selected == 4:
        for i in range(2):
            exp.as_pyplot_figure(label=int(selected_labels[i]))
            selected_columns_r1[i].pyplot()
            plt.clf()
        for i in range(2):
            exp.as_pyplot_figure(label=int(selected_labels[i+2]))
            selected_columns_r2[i].pyplot()
            plt.clf()
    else:        
        for i in range(total_selected):
            exp.as_pyplot_figure(label=int(selected_labels[i]))
            selected_columns[i].pyplot()
            plt.clf()
#======================RECOMMENDATION SYSTEM======================
if selected_side == "Recommendation System":
    st.subheader("About Recommendation System")
    st.write("Halaman ini akan menampilkan preferensi minuman sesuai dengan pilihan preferensi anda, terdapat contoh ekstraksi preferensi,table 10 preferensi minuman dengan nilai cosine teratas, dan contoh response yang diberikan oleh chatbot")
    with st.container():
        st.subheader("Variansi")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            jenis = st.selectbox("Jenis Minuman", ["Kopi", "Teh", "Mocktail", "Lainnya"])
        with col2:
            suhu = st.selectbox("Suhu", ["Dingin", "Panas"])
        with col3:
            susu = st.selectbox("Tambahan Susu", ["Iya", "Tidak"])
        with col4:
            sirup = st.selectbox("Tambahan Sirup", ["Iya", "Tidak"])
    with st.container():
        st.subheader("Tingkatan Rasa")
        st.write("Tingkatan rasa dimulai dari 1: Tidak, 2: Sedikit, 3: Sedang, 4: Kuat")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            manis = st.slider("Manis", min_value=1, max_value=4, value=2)
        with col2:
            pahit = st.slider("Pahit", min_value=1, max_value=4, value=2)
        with col3:
            asam = st.slider("Asam", min_value=1, max_value=4, value=2)
        with col4:
            gurih = st.slider("Gurih", min_value=1, max_value=4, value=2)

    preferences = f"{jenis} {suhu} {manis} {pahit} {asam} {gurih} {susu} {sirup}".lower()
    st.subheader("Preferensi User")
    st.write(f"Preferensi Minuman Anda: {preferences}")
    preferences = "/recommend " + preferences
    pref_prep = RSystem.preprocess_recommendation(preferences)
    df = RSystem.recommend_drinks(pref_prep, k=10, get_df=True)

    jenis_map = {1: "Kopi", 2: "Teh", 3: "Mocktails", 4: "Lainnya"}
    rasa_map = {1: "Tidak", 2: "Sedikit", 3: "Lumayan", 4: "Kuat"}
    ya_map = {0: "Tidak", 1: "Iya"}
    suhu_map = {0: "Panas", 1: "Dingin"}

    df["Jenis"] = df["Jenis"].map(jenis_map)
    df["Suhu"] = df["Suhu"].map(suhu_map)
    df["Manis"] = df["Manis"].map(rasa_map)
    df["Pahit"] = df["Pahit"].map(rasa_map)
    df["Asam"] = df["Asam"].map(rasa_map)
    df["Gurih"] = df["Gurih"].map(rasa_map)
    df["Susu"] = df["Susu"].map(ya_map)
    df["Sirup Buah"] = df["Sirup Buah"].map(ya_map)

    st.dataframe(df,use_container_width=True)

    st.subheader("Contoh Response")
    languages = st.selectbox("Pilih Bahasa", ["Indonesia", "Inggris"])
    if languages == "Indonesia":
        response = RSystem.response_br(preferences)
    else:
        response = RSystem.response_br_en(preferences)
    st.write(response)
    
