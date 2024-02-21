# Large Language Model Workshop

Contained within is the material to accompany the Large Language Model Workshop. Development of this material is an ongoing process, and given the rapid advancement of LLM libraries may contain bugs or out of date information. If you find any issues, please raise an Issue via GitHub, and we will endeavour to address it as soon as possible. Thank you!

## Contents
1. [Getting started](#getting-started)
    - [Colab](#api-keys)
    - [Local](#local)

2. [Introduction to APIs](#intro-to-APIs)
    - [Setting up API keys](#api-keys)
3. [Training and Augmenting GPT-2](#finetuning-gpt2)
4. [Finetuning for classification](#bert)
5. [No-code](#no-code)
6. [Stable Diffusion](#stable-diffusion)

## 1. Getting started <a id="getting-started"></a>

### Colab <a id="colab"></a>
Download the code from GitHub. Unzip the file and upload it to your Google Drive. In the beginning of the notebooks, there is an optional cell to run which will mount your drive and put you in the correct directory.

### Local <a id="local"></a>
Alternatively, if you're running locally, then just run
```python
pip install -r requirements.txt
```

## 2. Introduction to APIs <a id="intro-to-APIs"></a>
### Setting up API keys <a id="api-keys"></a>
Set up an OpenAI account, and a Hugging Face account. For the OpenAI account, you will need to enter credit card information in order to actually use the API!

You have some options when using the OpenAI API. You can either initialize the OpenAI client in this way:
```
client = OpenAI(api_key='YOUR_API_KEY')
```

or you can create a separate file called `.env` and store your API key in this way:
```
OPENAI_API_KEY = 'sk-1234567890'
```
and when you call `OpenAI()`, you key will be automatically read using `os.environ.get("OPENAI_API_KEY")`

## 3. Training and Augmenting GPT-2 <a id="finetuning-gpt2"></a>
A walkthrough of using and finetuning a Hugging Face model (GPT-2) can be found in the notebook `finetuning.ipynb`.

This notebook also contains code detailing the construction of a very simple RAG system.

## 4. Finetuning for classification <a id="bert"></a>
The notebook `BERT_classification.ipynb` contains some code for finetuning smaller models for classification or regression tasks using a simple dataset. It can be modified relatively easily to include your own data.

## 5. No-code <a id="no-code"></a>
In the workshop, we covered some no-code options:
- [LMStudio](https://lmstudio.ai/)
- [GPT4All](https://gpt4all.io/index.html)
- [Textgen-webui](https://github.com/oobabooga/text-generation-webui)

The easiest to get up and running is LMStudio. If you have a Macbook, it should be very easy to install. You experience with Windows may vary.

GPT4All is also relatively easy to install and get up and running.

Textgen-webui is capable of both inference and some fine-tuning. To get Textgen-webui up and running on your local machine is not too challenging. It is possible to run high-parameter models on the HPC or another remote cluster, and have access to the UI on your local machine. This can be more challenging, so if you're interested in doing this, and get stuck, get in touch with us.

## 6. Stable Diffusion <a id="stable-diffusion"></a>
You can find a very brief introduction to producing images with Stable Diffusion in the notebook titled `introduction_to_stable_diffusion.ipynb`. This should run on a Macbook or Colab.

In addition to the above no-code options, there is also [ComfyUI](https://github.com/comfyanonymous/ComfyUI), a UI for running Stable Diffusion model checkpoints and LoRAs. This will be slow when running on a laptop, but as with Textgen-webui, ComfyUI can also be run on a remote GPU. There are numerous tutorials online and on YouTube for ComfyUI ([here](https://stable-diffusion-art.com/comfyui/) for example).