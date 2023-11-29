## Instructions for running on colab

Two methods:
1. Download
2. Pip

## 1. Download
Download the code from GitHub. Unzip the file and upload it to your Google Drive. In the beginning of the notebooks, there is an optional cell to run which will mount your drive and put you in the correct directory.

## 2. Pip
Just run `!pip install something.something@something`

## General instructions
Alternatively, if you're running locally, then just run
```python
pip install -r requirements.txt
```

## API keys
Set up an OpenAI account, and a Hugging Face account. For the OpenAI account, you will need to enter credit card information in order to actually use the API!

You have some options when using the OpenAI API. You can either initialize the OpenAI client in this way:
```
client = OpenAI(api_key='YOUR_API_KEY')
```

or you can create a separate file called `.env` and store your API key in this way:
```
OPENAI_API_KEY = 'sk-1234567890'
```
and when you call `OpenAI()`, you key will be automatically read using `os.environ.get("OPENAI_API_KEY")``
