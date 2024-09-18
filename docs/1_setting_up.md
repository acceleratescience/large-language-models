# Setting up

For this workshop, we will be using models from OpenAI. We understand that often in research, we want full control and ownership over our models. The models hosted by OpenAI are closed source, and therefore may be inappropriate for some use cases. However, there are some advantages to using OpenAI models:

1. OpenAI arguably offer the best current models
2. The documentation is excellent
3. They use the OpenAI API spec.

The final point is particularly important - we will show you how to set up a cloud instance on RunPod using vLLM. vLLM is a library that essentially wraps a hugging face model in an API spec that is compatible with OpenAI. So almost all of the skills you learn using OpenAI will be transferable to running your own models.

If you want to use OpenAI, you will need to create an API key. For this workshop, we will provide you with one. However, if you want to use your own open source models, then you can also do that. During the workshop, wherever possible, we will try and highlight the differences between using OpenAI and your own models.

## Setting up your environment
For this workshop, since we're not really doing any heavy lifting, we can work entirely within Github Codespaces. If you want, you can also use any other IDE you like, such as VSCode, or Jupyter Notebooks.

My advice would be to create a new repository on Github, and then create a codespace from that repository. You can then copy and past the `requirements-handson.txt` file into the repository, and install the dependencies. You can also copy and paste the `Handson` folder into your repository. This folder contains the code that we will run through in the workshop.

```bash
pip install -r requirements-handson.txt
```

You should also create a new file called `.env` and add your OpenAI API key to it.

```bash
OPENAI_API_KEY=<YOUR_API_KEY>
```

## Setting up RunPod and vLLM
For this demonstration we will run `llama-3.1-8b` on a Nvidia A40 GPU. If you want to do this, you will need to set up a RunPod account, add a payment method, and deposit some credit. For RunPod, you pay by the hour.

**1. Create a RunPod account** Head to the [runpod website](https://www.runpod.io/) and create an account.

**2. Over to `Billing` and add some credit** You can add a payment method and deposit any amount you like.

**3. Gain access to Llama 3.1** You will need to request access to the Llama 3.1 models. You can do this by heading over to the [Hugging Face site](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B). You'll need to log in and request access. It's usually pretty quick, but it can take a day or two.

**4. Create a RunPod Template** Head to templates and add a new template. Fill out the details as shown below.

![RunPod Template](imgs/template.png)

For the token you'll need to add a new Hugging Face API token. You can create one [here](https://huggingface.co/settings/tokens).

![RunPod Secret](imgs/secret.png)

**5. Create a Pod** Once your template has been set, you can create a Pod. Head to `Pods` and click `+ Deploy`. Select the Nvidia A40 and the Llama 3.1 template you created earlier. The pod will take a while to to start up, but when it does you should see something like the below image

![Connect Pod](imgs/connect.png)

Hit `Connect` and then `Connect to HTTP Service [Port 8000]`. You will be directed to a confusing looking page that just says `{"detail":"Not Found"}`. Don't worry, this is normal. Copy the URL that is in the browser bar. This is your API endpoint.

### Connect to your API endpoint

Now we can connect to our API endpoint. Fire up a Jupyter notebook, and try running the following, pasting in the URL you copied earlier.

```python
from openai import OpenAI

model = "meta-llama/Meta-Llama-3.1-8B-Instruct"
base_url = <ENTER YOUR URL HERE>

openai_api_key = "EMPTY"
openai_api_base = base_url + "v1"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)
```

This sets up the client.


```python

system_prompt_base = "You are a helpful assistant."

completion = client.chat.completions.create(
    model=model,
    messages= [
            {"role": "system", "content": system_prompt_base},
            {"role": "user", "content": "Hello, how are you?"}
        ],
    max_tokens=256,
    stream=True,
    temperature=0.6,
    stop="<|eot_id|>"
)

# completion.choices[0].message.content

for chunk in completion:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
```

If you switch back to the RunPod terminal, you should see some activity showing throughput (the number of tokens per second).

If you get any errors, the RunPod terminal is the best place to see what went wrong.

You can switch out Llama 3.1 for any of the other [models supported by vLLM](https://docs.vllm.ai/en/latest/models/supported_models.html). Please note that not all of these models will have the same level of support. You might also find subtle differences. For example: the MistralAI models do not have an explicit system prompt; and some models have different context window limits that you may need to set manually in the RunPod template. If you are having trouble with a particular model, please feel free to ask for help.
