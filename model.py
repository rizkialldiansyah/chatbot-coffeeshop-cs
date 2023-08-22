import torch
import torch.nn as nn

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, dropout_rate=0.5, embedding_matrix=None):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size

        # Dropout layer
        self.dropout = nn.Dropout(dropout_rate)

        # Word Embedding layer
        self.embedding = nn.Embedding.from_pretrained(embedding_matrix)

        # LSTM weights
        self.W_xi = nn.Parameter(torch.empty(input_size, hidden_size))
        self.W_xf = nn.Parameter(torch.empty(input_size, hidden_size))
        self.W_xo = nn.Parameter(torch.empty(input_size, hidden_size))
        self.W_xc = nn.Parameter(torch.empty(input_size, hidden_size))
        self.W_hi = nn.Parameter(torch.empty(hidden_size, hidden_size))
        self.W_hf = nn.Parameter(torch.empty(hidden_size, hidden_size))
        self.W_ho = nn.Parameter(torch.empty(hidden_size, hidden_size))
        self.W_hc = nn.Parameter(torch.empty(hidden_size, hidden_size))
        self.W_hy = nn.Parameter(torch.empty(hidden_size, output_size))
        
        # Bias terms
        self.b_i = nn.Parameter(torch.empty(hidden_size))
        self.b_f = nn.Parameter(torch.empty(hidden_size))
        self.b_o = nn.Parameter(torch.empty(hidden_size))
        self.b_c = nn.Parameter(torch.empty(hidden_size))
        self.b_hi = nn.Parameter(torch.empty(hidden_size))
        self.b_hf = nn.Parameter(torch.empty(hidden_size))
        self.b_ho = nn.Parameter(torch.empty(hidden_size))
        self.b_hc = nn.Parameter(torch.empty(hidden_size))
        self.b_hy = nn.Parameter(torch.empty(output_size))

        # Initialize parameters
        self.reset_parameters()

    def reset_parameters(self):
        # Initialize weights using Xavier initialization and biases with zeros
        nn.init.xavier_uniform_(self.W_xi)
        nn.init.xavier_uniform_(self.W_xf)
        nn.init.xavier_uniform_(self.W_xo)
        nn.init.xavier_uniform_(self.W_xc)
        nn.init.xavier_uniform_(self.W_hi)
        nn.init.xavier_uniform_(self.W_hf)
        nn.init.xavier_uniform_(self.W_ho)
        nn.init.xavier_uniform_(self.W_hc)
        nn.init.xavier_uniform_(self.W_hy)
        
        nn.init.zeros_(self.b_i)
        nn.init.zeros_(self.b_f)
        nn.init.zeros_(self.b_o)
        nn.init.zeros_(self.b_c)
        nn.init.zeros_(self.b_hi)
        nn.init.zeros_(self.b_hf)
        nn.init.zeros_(self.b_ho)
        nn.init.zeros_(self.b_hc)
        nn.init.zeros_(self.b_hy)

    def forward(self, input):
        batch_size, seq_len = input.size()
        hidden_state = torch.zeros(batch_size, self.hidden_size)
        cell_state = torch.zeros(batch_size, self.hidden_size)

        for t in range(seq_len):
            x = self.embedding(input[:, t])  # Embedding input
            x = self.dropout(x)

            # Input gate
            i = torch.sigmoid(torch.mm(x, self.W_xi) + torch.mm(hidden_state, self.W_hi) + self.b_i)

            # Forget gate
            f = torch.sigmoid(torch.mm(x, self.W_xf) + torch.mm(hidden_state, self.W_hf) + self.b_f)

            # Output gate
            o = torch.sigmoid(torch.mm(x, self.W_xo) + torch.mm(hidden_state, self.W_ho) + self.b_o)

            # Cell state candidate
            c_candidate = torch.tanh(torch.mm(x, self.W_xc) + torch.mm(hidden_state, self.W_hc) + self.b_c)

            # Update cell state
            cell_state = f * cell_state + i * c_candidate

            # Update hidden state
            hidden_state = o * torch.tanh(cell_state)

        output = torch.mm(hidden_state, self.W_hy) + self.b_hy
        return output