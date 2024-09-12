# Setting up

For this workshop, we will be using models from OpenAI. We understand that often in research, we want full control and ownership over our models. The models hosted by OpenAI are closed source, and therefore may be inappropriate for some use cases. However, there are some advantages to using OpenAI models:

1. OpenAI arguably offer the best current models
2. The documentation is excellent
3. They use the OpenAI API spec.

The final point is particularly important - we will show you how to set up a cloud instance on RunPod using vLLM. vLLM is a library that essentially wraps a hugging face model in an API spec that is compatible with OpenAI. So almost all of the skills you learn using OpenAI will be transferable to running your own models.

If you want to use OpenAI, you will need to create an API key. For this workshop, we will provide you with one. However, if you want to use your own open source models, then you can also do that. During the workshop, wherever possible, we will try and highlight the differences between using OpenAI and your own models.

## Setting up your environment
For this workshop, since we're not really doing any heavy lifting, we can work entirely within Github Codespaces. If you want, you can also use any other IDE you like, such as VSCode, or Jupyter Notebooks.

My advice would be to create a new repository on Github, and then create a codespace from that repository. You can then copy and past the `requirements-handson.txt` file into the repository, and run

```bash
pip install -r requirements-handson.txt
```

## Setting up RunPod and vLLM
For this demonstration we will run `llama-3.1-8b` on a Nvidia A40 GPU. If you want to do this, you will need to set up a RunPod account, add a payment method, and deposit some credit. For RunPod, you pay by the hour.

