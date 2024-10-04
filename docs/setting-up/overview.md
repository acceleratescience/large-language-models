# Overview

For the in-person workshop, we will be using models from OpenAI. We understand that often in research, we want full control and ownership over our models. The models hosted by OpenAI are closed source, and therefore may be inappropriate for some use cases. However, there are some advantages to using OpenAI models:

1. OpenAI arguably offer the best current models
2. They are reliable
3. The documentation is excellent
4. They use the OpenAI API spec

The final point is particularly important - many popular endpoints make use of the OpenAI API spec. For example, vLLM is a library that essentially wraps a hugging face model in an API spec that is compatible with OpenAI; Microsoft Azure AI Studio, Google Vertex AI, Amazon AWS Bedrock all offer ways to serve models using vLLM.

So almost all of the skills you learn using OpenAI's models will be transferable to running your own models.

If you want to use OpenAI, you will need to create an API key. For the in-person workshop, we will provide you with one. However, if you want to use your own open source models, then you can also do that. During the workshop, wherever possible, we will try and highlight the differences between using OpenAI and your own models.

We offer an overview of how to setup various environments:

- GitHub Codespaces
- RunPod
- Nvidia NIMs
- Microsoft Azure AI Studio

Pick one on the left-hand sidebar. More may be added in the future.