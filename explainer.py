import lime
import lime.lime_text
from lime.lime_text import LimeTextExplainer
import torch
from model import LSTMModel
from util.input_prep import text_cleansing, slang_processing, stemming, remove_stopwords, text_to_padded_indices

class LimeExplainer:
    def __init__(self, file_path):
        variable_data = torch.load(file_path)

        self.input_size = variable_data["input_size"]
        self.output_size = variable_data["output_size"]
        self.hidden_size = variable_data["hidden_size"]
        self.model_state = variable_data["model_state"]
        self.class_names = variable_data["class_names"]

        self.embedding_matix = variable_data["embedding_matix"]
        self.word_idx = variable_data["word_idx"]
        self.seq_length = variable_data["seq_size"]

        self.model = LSTMModel(self.input_size, self.hidden_size, self.output_size, embedding_matrix=self.embedding_matix)
        self.model.load_state_dict(self.model_state)
        self.model.eval()

        self.explainer = LimeTextExplainer(class_names=self.class_names)

    def text_prep(self, text):
        processed_text = text_cleansing(text)
        processed_text = slang_processing(processed_text)
        processed_text = stemming(processed_text)
        processed_text = remove_stopwords(processed_text)
        return processed_text

    def predict_proba(self, texts):
        texts = [text_cleansing(text) for text in texts]
        text_indices = [text_to_padded_indices(text, self.word_idx, self.seq_length) for text in texts]
        text_indices_tensor = torch.tensor(text_indices)

        with torch.no_grad():
            logits = self.model(text_indices_tensor)
            probas = torch.softmax(logits, dim=1).numpy()
        return probas
