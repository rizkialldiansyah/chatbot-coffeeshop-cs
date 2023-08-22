import torch
import random
import json
from model import LSTMModel
from util.input_prep import text_cleansing, slang_processing, stemming, remove_stopwords, text_to_padded_indices

class McobotChatbot:
    def __init__(self):
        self.bot_name = "Mcobot"
        self.load_data()
        self.load_lstm_model()

    def load_data(self):
        path_indo = "./data/indo/dataset_indonesia.json"
        with open(path_indo) as data_file:
            self.data_indonesia = json.load(data_file)

    def load_lstm_model(self):
        FILE = "./var/data_var_id.pth"
        variable_data = torch.load(FILE)

        input_size = variable_data["input_size"]
        output_size = variable_data["output_size"]
        hidden_size = variable_data["hidden_size"]
        model_state = variable_data["model_state"]
        index_target = variable_data["index_target"]
        embedding_matix = variable_data["embedding_matix"]
        self.word_idx = variable_data["word_idx"]
        self.seq_length = variable_data["seq_size"]

        self.model = LSTMModel(input_size, hidden_size, output_size, embedding_matrix=embedding_matix)
        self.model.load_state_dict(model_state)
        self.model.eval()
        self.index_target = index_target

    def text_prep(self, chat_input):
        chat_prep = text_cleansing(chat_input)
        chat_slang = slang_processing(chat_prep)
        chat_stemmed = stemming(chat_slang)
        chat_unstopword = remove_stopwords(chat_stemmed)
        pad_seq = text_to_padded_indices(chat_unstopword, self.word_idx, self.seq_length)
        return pad_seq

    def NLU_engine(self, input_tensor):
        with torch.no_grad():
            # Memindahkan tensor input ke perangkat yang sama dengan model
            device = next(self.model.parameters()).device
            input_tensor = input_tensor.to(device)
            # Melakukan prediksi pada data uji
            output = self.model(input_tensor)
            predicted_indices = torch.argmax(output, dim=1)
            pred = predicted_indices[0].item()
            probs = torch.softmax(output, dim=1)
            prob = probs[0][pred]
            print(prob.item())
            
            if prob < 0.8:
                return ['dont_understand']
            
        return [key for key, value in self.index_target.items() if value == pred]

    def get_response(self, msg):
        # Preprocessing text
        pad_seq = [self.text_prep(msg)]
        data_tensor = torch.tensor(pad_seq)
        # NLU
        intent = self.NLU_engine(data_tensor)

        # Get responses data by languages
        for tg in self.data_indonesia['intents']:
            if tg['tag'] == intent[0]:
                return random.choice(tg['responses'])
            elif intent[0] == "dont_understand":
                return "Maaf, saya agak kesulitan memahami pesan yang Anda kirim.\nApakah Anda bisa mengirimkan pesan dengan kalimat yang berbeda agar saya bisa membantu Anda dengan lebih baik?"

    def chat_loop(self):
        print(f"Let's chat with {self.bot_name}! (type 'quit' to exit)")
        while True:
            sentence = input("You: ")
            if sentence == "quit":
                break
            resp = self.get_response(sentence)
            print(f"{self.bot_name}: {resp}")

if __name__ == "__main__":
    chatbot = McobotChatbot()
    chatbot.chat_loop()
