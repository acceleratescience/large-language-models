from transformers import AutoTokenizer, AutoModel
import torch


class Embedder:
    def __init__(self, model_name : str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        # max input size
        self.max_length = self.model.config.max_position_embeddings


    def __call__(self, text_list : list, batch_size : int = 32) -> torch.Tensor :
        """Generates the embedding of the input texts using the specified model and tokenizer.

        Args:
            text_list (list): A list of texts to embed.

        Returns:
            torch.Tensor: The embedding of the input text.
        """
        
        tokens = [self.tokenizer.tokenize(text) for text in text_list]
        # inputs = self.tokenizer(text_list, padding=True, return_tensors="pt", add_special_tokens=True)

        embeddings = []
        for i in range(0, len(text_list), batch_size):
            inputs = self.tokenizer(text_list[i:i+batch_size], padding=True, return_tensors="pt", add_special_tokens=True)
            batch_inputs = {key: val for key, val in inputs.items()}

            for key, val in batch_inputs.items():
                batch_inputs[key] = val.to(self.device)
            with torch.no_grad():
                last_hidden_states = self.model(**batch_inputs, output_hidden_states=True).last_hidden_state
            embeddings.append(last_hidden_states)

        max_len = max([batch.shape[1] for batch in embeddings])

        for i in range(len(embeddings)):
            embeddings[i] = torch.nn.functional.pad(embeddings[i], (0,0,0,max_len-embeddings[i].shape[1]), 'constant', 0)

        embeddings = torch.cat(embeddings, dim=0)


        return tokens, embeddings

        # with torch.no_grad():
        #     last_hidden_states = self.model(**inputs, output_hidden_states=True).last_hidden_state

        # return tokens, last_hidden_states
