from types import SimpleNamespace
import warnings
warnings.filterwarnings("ignore") # I'm sure this will be fine...

from transformers import TextDataset, DataCollatorForLanguageModeling
from transformers import AutoTokenizer, AutoModelWithLMHead
from transformers import Trainer, TrainingArguments
from transformers import DataCollatorForLanguageModeling

import torch
from datasets import Dataset

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS


class Agent():
    def __init__(self, model_config : SimpleNamespace, database_config : SimpleNamespace = None):
        """RAG agent

        Args:
            model_config (SimpleNamespace): model parameters
            database_config (SimpleNamespace, optional): database parameters. Defaults to None.
        """
        self.model_config = model_config
        self._validate_model_config()
        self.database_config = database_config

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        print(f"Initalizing model: {self.model_config.model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_config.model_name)
        self.model = AutoModelWithLMHead.from_pretrained(self.model_config.model_name).to(self.device)

        if self.database_config is not None:
            print(f"Creating database from: {self.database_config.text_path}")
            self.db = self._create_database()

        self.trained = False

    
    def __repr__(self):
        agent_config = f"self.model_config: {self.model_config}\nself.database_config: {self.database_config}"
        return agent_config


    def _validate_model_config(self):
        assert hasattr(self.model_config, 'model_name'), "model_config must have a model_name attribute"
        if not hasattr(self.model_config, 'gen_length'):
            self.model_config.gen_length = 128
        if not hasattr(self.model_config, 'context_length'):
            self.model_config.context_length = 256
        if not hasattr(self.model_config, 'temperature'):
            self.model_config.temperature = 0.7
        if not hasattr(self.model_config, 'do_sample'):
            self.model_config.do_sample = True

    
    def _validate_database_config(self):
        assert hasattr(self.database_config, 'text_path'), "database_config must have a text_path attribute"
        assert hasattr(self.database_config, 'text_splitter'), "database_config must have a text_splitter attribute"
        assert hasattr(self.database_config, 'chunk_size'), "database_config must have a chunk_size attribute"
        assert hasattr(self.database_config, 'chunk_overlap'), "database_config must have a chunk_overlap attribute"
        assert hasattr(self.database_config, 'embedding_model'), "database_config must have an embedding_model attribute"
        assert hasattr(self.database_config, 'vector_store'), "database_config must have a vector_store attribute"
            
    
    def _create_database(self):
        self._validate_database_config()
        
        with open(self.database_config.text_path, 'r') as f:
            text = f.read()

        # Split text
        text_splitter = self.database_config.text_splitter(
            separator=' ',
            chunk_size=self.database_config.chunk_size,
            chunk_overlap=self.database_config.chunk_overlap,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        embeddings = HuggingFaceEmbeddings(model_name=self.database_config.embedding_model)
        db = self.database_config.vector_store.from_texts(chunks, embeddings)

        return db


    def ask_question(self, query : str = "What is your name?", retrieval : bool = True) -> str:
        """Ask a question

        Args:
            query (str, optional): Query to the Agent. Defaults to "What is your name?".

        Returns:
            str: Output string from the Agent
        """
        question = "QUESTION: " + query

        if retrieval and self.database_config is not None:
            docs = self.db.similarity_search(query, k=3)
            prompt = " ".join([doc.page_content for doc in docs]) + "\n\n" + question + " RESPONSE:"
        else:
            prompt = question + " RESPONSE:"

        input_ids = self.tokenizer.encode(prompt, return_tensors='pt').to(self.device)

        output = self.model.generate(input_ids,
                        max_length=self.model_config.gen_length + len(input_ids[0]),
                        # temperature=0.7,
                        num_beams=5,
                        no_repeat_ngram_size=2,
                        early_stopping=True,
                        # do_sample=True,
                        pad_token_id=self.tokenizer.pad_token_id   
                    )

        # output without input_ids
        return self.tokenizer.decode(output[0][len(input_ids[0]):], skip_special_tokens=True)[1:]


    def train(self, training_config : SimpleNamespace) -> None:
        """Train the Agent using the given training_config

        Args:
            training_config (SimpleNamespace): Training hyperparameters

        Returns:
            None
        """
        if not self.trained:
            self.tokenizer.add_special_tokens({'pad_token': '<pad>'})
            with torch.no_grad():
                self.model.resize_token_embeddings(len(self.tokenizer))
            self.model.config.pad_token_id = self.tokenizer.pad_token_id

        data = Dataset.from_text(training_config.dataset_path, split='train')
        
        outputs = self.tokenizer(
                data["text"],
                truncation=True,
                max_length=training_config.context_length,
                return_overflowing_tokens=True,
                return_length=True,
            )

        {"input_ids": outputs.input_ids}

        tokenized_dataset = Dataset.from_dict({"input_ids": outputs.input_ids})

        data_collator = DataCollatorForLanguageModeling(self.tokenizer, mlm=False)

        args = TrainingArguments(
            output_dir="./results",
            per_device_train_batch_size=training_config.batch_size,
            num_train_epochs=training_config.num_epochs,
            logging_steps=100
        )

        trainer = Trainer(
            model=self.model,
            tokenizer=self.tokenizer,
            args=args,
            data_collator=data_collator,
            train_dataset=tokenized_dataset,
        )

        trainer.train()

        self.trained = True