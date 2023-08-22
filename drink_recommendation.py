import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class DrinkRecommendationSystem:
    def __init__(self, menu_data_file):
        self.minuman_df = pd.read_csv(menu_data_file)
        self.weights = np.array([[0.29, 0.15, 0.115, 0.115, 0.115, 0.115, 0.05, 0.05]])

    # Fungsi untuk menghapus duplikasi huruf dalam sebuah kata
    def remove_duplicate_letters(self, word):
        new_word = word[0]
        for i in range(1, len(word)):
            if word[i] != word[i-1]:
                new_word += word[i]
        return new_word

    def is_numeric(self, input_string):
        return input_string.isdigit()

    def weighted_cosine_similarity(self, user_preferences):
        scaler = MinMaxScaler()
        menu_scaled = scaler.fit_transform(self.minuman_df.iloc[:, 1:].values)
        user_scaled = scaler.transform(np.array(user_preferences))

        menu_vectors = menu_scaled * self.weights
        user_vector = user_scaled * self.weights

        dot_product = np.dot(user_vector, menu_vectors.T)
        user_magnitude = np.linalg.norm(user_vector)
        menu_magnitudes = np.linalg.norm(menu_vectors, axis=1)

        cosine_similarity = dot_product / (user_magnitude * menu_magnitudes)

        return cosine_similarity

    def recommend_drinks(self, user_preferences, k=7, get_df=False):
        cosine_similarity = self.weighted_cosine_similarity(user_preferences)
        top_k_indices = np.argsort(cosine_similarity)[0][-k:][::-1]

        # Buat DataFrame dengan hasil rekomendasi dan cosine similarity
        if get_df == True:
            recommended_df = self.minuman_df.loc[top_k_indices].reset_index(drop=True)
            recommended_df['Cosine Similarity'] = cosine_similarity[0][top_k_indices]
            return recommended_df
        
        return self.minuman_df.loc[top_k_indices].reset_index(drop=True)

    def preprocess_recommendation(self, input_string):
        input_string = input_string.lower()
        input_words = input_string.split()[1:]

        keywords = {
            "kopi": ["kopi", "kop", "kp", "kpi","kopy","koopi","kopee","koppi","kopie","koffi","cofi","coffe","cofie","coffie","coffe","cofe","coffie","coffy","coofee","kofi","koffi","koffee","koffie","kofie","coffee"],
            "teh": ["teh", "the", "th", "tae","teb","teah","teu", "te"],
            "mocktail": ['mocktail', "moctail", "mochtail","moktail","moktel","mocktale","mokktail","moktail","moktail","mokctail","mokctel","moktel","mokatail"],
            "lainnya": ['lainnya','laenir','laenya','laenya','lainya','lainyah','lainyra','lanery','laninya','lanir','lanira','lanya','lanyra','lenya','lianry','lianya','lny','lnya','lynera','lynira','lynya'],
            "panas": ['hot', 'ht', 'hto','pana','panas','panaz','panis','pans','pansa','pansis','pas','pasnas','penas','phnas','pn','pnanas','pnas','pns','psnas','pamas','pmas'],
            "dingin": ['cold', 'cool', 'cld', 'cod', 'dengin','dgn','digin','diginh','dign','ding','dinga','dingan','dingen','dingenin','dingi','dingin','dingina','dinginh','dingiun','dingn','dingng','dingun','dinign','dinkin','dng','dngin','dngn'],
            "iya": ['yes', 'eiy','ey','ia','iea','iey','ieya','iy','iya','iyaha','y','ya','yah','yak','ye','yea','yeah','yia','yiya','yoi','yup','iah','iyah','yh','iyh'],
            "tidak": ['no','nope','not','np','nop','none','ega','eng','enga','engga','mgga','emgga','enggak', 'engak','g','ga','gak','ndak','ng','nga','ngak','ngaq','tak','tdak','tdk','tida','tidah','tidak','tidap','tidaq','tidk'],
        }

        preference = {
            "jenis": "kopi",
            "suhu": "dingin",
            "rasa": [4, 2, 1, 2], # manis, pahit, asam, gurih
            "variasi": ["iya", "tidak"], # susu, fs
        }

        rasa = []
        variasi = []
        for word in input_words:
            if self.is_numeric(word):
                rasa.append(word)
            else:
                word = self.remove_duplicate_letters(word)
                for key, value in keywords.items():
                    if word in value:
                        if key == "kopi" or key == "teh" or key == "mocktail" or key == "lainnya":
                            preference["jenis"] = key
                        elif key == "dingin" or key == "panas":
                            preference["suhu"] = key
                        elif key == "iya" or key == "tidak":
                            variasi.append(key)

        preference["variasi"] = variasi
        preference["rasa"] = rasa
        preference_values = []
        for key in preference:
            if key == "rasa":
                for i in preference[key]:
                    preference_values.append(int(i))
            elif key == "jenis":
                if preference[key] == "kopi":
                    preference_values.append(1)
                elif preference[key] == "teh":
                    preference_values.append(2)
                elif preference[key] == "mocktail":
                    preference_values.append(3)
                elif preference[key] == "lainnya":
                    preference_values.append(4)
            elif key == "suhu":
                if preference[key] == "dingin":
                    preference_values.append(1)
                elif preference[key] == "panas":
                    preference_values.append(0)
            elif key == "variasi":
                for i in preference[key]:
                    if i == "iya":
                        preference_values.append(1)
                    else:
                        preference_values.append(0)

        return np.array([preference_values])

    def response_br(self, input_string):
        user_preferences = self.preprocess_recommendation(input_string)
        recommended_table = self.recommend_drinks(user_preferences)

        jenis = {1: "kopi", 2: "teh", 3: "mocktails", 4: "lainnya"}
        rasa = {1: "tidak", 2: "sedikit", 3: "lumayan", 4: ""}
        ya = {0: "tidak", 1: ""}
        suhu = {0: "panas", 1: "dingin"}

        statement = "Rekomendasi minuman sesuai preferensi Anda:\n"
        for i, row in recommended_table.iterrows():
            statement += f"{i+1}. **{row['Menu']}**, {suhu[row['Suhu']]} {jenis[row['Jenis']]} dengan rasa manis {rasa[row['Manis']]}, pahit {rasa[row['Pahit']]}, asam {rasa[row['Asam']]}, dan gurih {rasa[row['Gurih']]}.\n"
            if row['Susu'] == 1:
                statement += "Minuman ini menggunakan tambahan susu. "
            if row['Sirup Buah'] == 1:
                statement += "Minuman ini memiliki rasa buah.\n"
            else:
                statement += "\n"
        return statement
    
    def response_br_en(self, input_string):
        user_preferences = self.preprocess_recommendation(input_string)
        recommended_table = self.recommend_drinks(user_preferences)

        jenis = {1: "coffee", 2: "tea", 3: "mocktails", 4: "another"}
        rasa = {1: "not", 2: "a bit", 3: "moderate", 4: ""}
        suhu = {0: "hot", 1: "cold"}

        statement = "Drink recommendations according to your preferences:\n"
        for i, row in recommended_table.iterrows():
            statement += f"{i+1}. **{row['Menu']}**, {suhu[row['Suhu']]} {jenis[row['Jenis']]} with {rasa[row['Manis']]} sweet taste, {rasa[row['Pahit']]} bitter,{rasa[row['Asam']]} sour, and {rasa[row['Gurih']]} savory.\n"
            if row['Susu'] == 1:
                statement += "This drink uses added milk."
            if row['Sirup Buah'] == 1:
                statement += "This drink has a fruity taste.\n"
            else:
                statement += "\n"
        return statement