from types import SimpleNamespace

import torch
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModel, AutoTokenizer

from datasets import load_dataset

from .embedder import Classifier
from .embedding_dataset import TextClassificationDataset


def get_device():
    if torch.cuda.is_available():
        return torch.device('cuda')
    # For M1 Macs
    elif torch.backends.mps.is_available():
        return torch.device('mps')
    else:
        return torch.device('cpu')

def sentiment2label(sentiment):
    return 'positive' if sentiment == 1 else 'negative'

def label2sentiment(label):
    return 1 if label == 'positive' else 0

def clean_text(text):
    return text.replace('<br />', ' ')

def get_text_and_labels(data):
    texts = [clean_text(sample['text']) for sample in data]
    labels = [sample['label'] for sample in data]
    return texts, labels

def get_train_test_data():
    dataset = load_dataset('imdb')
    texts, labels = get_text_and_labels(dataset['train'])
    test_texts, test_labels = get_text_and_labels(dataset['test'])

    return texts, labels, test_texts, test_labels

def get_train_test_loaders(texts, labels, test_texts, test_labels, tokenizer, max_len, batch_size):
    train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2)

    train_dataset = TextClassificationDataset(train_texts, train_labels, tokenizer, max_len)
    val_dataset = TextClassificationDataset(val_texts, val_labels, tokenizer, max_len)
    test_dataset = TextClassificationDataset(test_texts, test_labels, tokenizer, max_len)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, test_loader


def train_epoch(model, train_loader, criterion, optimizer, device):
    model.train()
    train_loss = 0
    for batch in train_loader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['label'].to(device)

        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
    train_loss /= len(train_loader)
    accuracy = accuracy_score(all_labels, all_preds)

    return train_loss, accuracy


def eval_model(model, val_loader, criterion, device):
    model.eval()
    val_loss = 0
    all_labels = []
    all_preds = []
    with torch.no_grad():
        for batch in val_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)

            outputs = model(input_ids, attention_mask)
            loss = criterion(outputs, labels)
            val_loss += loss.item()

            preds = torch.argmax(outputs, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    val_loss /= len(val_loader)
    accuracy = accuracy_score(all_labels, all_preds)
    return val_loss, accuracy


def train_model(model, train_loader, val_loader, criterion, optimizer, device, n_epochs):
    for epoch in range(n_epochs):
        train_loss, train_accuracy = train_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_accuracy = eval_model(model, val_loader, criterion, device)
        print(f'Epoch {epoch + 1}/{n_epochs}, Train Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.4f}, Val Loss: {val_loss:.4f}, Val Accuracy: {val_accuracy:.4f}')


def main(params):
    device = get_device()
    tokenizer = AutoTokenizer.from_pretrained(params.embedding_model)
    print("Getting data...")
    texts, labels, test_texts, test_labels = get_train_test_data()
    train_loader, val_loader, test_loader = get_train_test_loaders(texts, labels, test_texts, test_labels, tokenizer, params.max_len, params.batch_size)

    print("Building model...")
    model = Classifier(params.embedding_model, 2, params.dropout_p, params.train_embedder).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=params.lr)

    print("Training model...")
    train_model(model, train_loader, val_loader, criterion, optimizer, device, params.n_epochs)

    print("Evaluating model...")
    test_loss, test_accuracy = eval_model(model, test_loader, criterion, device)
    print(f'Test Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy:.4f}')