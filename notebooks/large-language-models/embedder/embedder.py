import torch
from torch import nn
from transformers import AutoModel


class Classifier(nn.Module):
    def __init__(self, embedding_model, n_classes, dropout_p=0.1, train_embedder=True):
        super().__init__()
        self.embedding_model = AutoModel.from_pretrained(embedding_model)
        self.dropout = nn.Dropout(dropout_p)
        self.linear = nn.Linear(self.embedding_model.config.hidden_size, n_classes)

        if not train_embedder:
            for param in self.embedding_model.parameters():
                param.requires_grad = False

    def forward(self, input_ids, attention_mask):
        outputs = self.embedding_model(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = outputs.last_hidden_state
        pooled_output = last_hidden_state[:, 0]
        pooled_output = self.dropout(pooled_output)
        logits = self.linear(pooled_output)
        return logits