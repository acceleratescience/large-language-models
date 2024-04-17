<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<!-- PROJECT SHIELDS -->
<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL License][license-shield]][license-url] -->
[![MIT License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/)
[![Issues](https://img.shields.io/github/issues-raw/acceleratescience/large-language-models.svg?maxAge=25000)](https://github.com/acceleratescience/large-language-models/issues)
[![GitHub contributors](https://img.shields.io/github/contributors/acceleratescience/large-language-models.svg?style=flat)]()
[![GitHub pull requests](https://img.shields.io/github/issues-pr/acceleratescience/large-language-models.svg?style=flat)]()
[![PR's Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)
<br>
[![GitHub stars](https://img.shields.io/github/stars/acceleratescience/large-language-models.svg?style=social&label=Star)]()
[![GitHub watchers](https://img.shields.io/github/watchers/acceleratescience/large-language-models.svg?style=social&label=Watch)]()
[![GitHub forks](https://img.shields.io/github/forks/acceleratescience/large-language-models.svg?style=social&label=Fork)](https://github.com/JonSnow/MyBadges)
[![GitHub followers](https://img.shields.io/github/followers/acceleratescience.svg?style=social&label=Follow)](https://github.com/JonSnow/MyBadges)
[![Twitter Follow](https://img.shields.io/twitter/follow/AccelerateSci.svg?style=social)](https://twitter.com/AccelerateSci)
<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://acceleratescience.github.io/">
    <img src="./images/full_acc.png" alt="Logo" height=80>
  </a>

  <h3 align="center">Large Language Models for Scientific Research</h3>

  <p align="center">
    An introduction to large language models for scientific research - how do they work, how can they be used, and how can they be trained?
    <br />
    <!-- <a href="https://acceleratescience.github.io/packaging-publishing/"><strong>Start the Course »</strong></a>
    <br />
    <br />
    <a href="https://github.com/acceleratescience/packaging-publishing/tree/basic">Get Basic Code</a>
    · -->
    <a href="https://github.com/acceleratescience/large-language-models/issues">Report Bug</a>
    ·
    <a href="https://github.com/acceleratescience/large-language-models/issues">Request Content</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li>
        <a href="#gettingstarted">Getting Started</a>
        <ol>
            <li><a href="#colab">Colab</a></li>
            <li><a href="#local">Local</a></li>
        </ol>
    </li>
    <li><a href="#intro-to-APIs">Setting up API Keyes</a></li>
    <li><a href="#finetuning-gpt2">Training and Augmenting GPT-2</a></li>
    <li><a href="#bert">Finetuning for classification</a></li>
    <li><a href="#no-code">No-code</a></li>
    <li><a href="#stable-diffusion">Stable Diffusion</a></li>
  </ol>
</details>



<!---------------------------------------------------------------------------->

[Button Shield]: https://img.shields.io/badge/Shield_Buttons-37a779?style=for-the-badge

[License]: LICENSE
[Shield]: Types/Shield.md
[#]: #


<!---------------------------------[ Badges ]---------------------------------->

[Badge License]: https://img.shields.io/badge/-BY_SA_4.0-ae6c18.svg?style=for-the-badge&labelColor=EF9421&logoColor=white&logo=CreativeCommons
[Badge Likes]: https://img.shields.io/github/stars/MarkedDown/Buttons?style=for-the-badge&labelColor=d0ab23&color=b0901e&logoColor=white&logo=Trustpilot



<!-- GETTING STARTED -->
## Prerequisites
This project requires some prerequisites in terms of skill level: you should be proficient with Python and PyTorch, and some understanding of git would be helpful.

Development of this material is an ongoing process, and given the rapid advancement of LLM libraries may contain bugs or out of date information. If you find any issues, please raise an Issue via GitHub, and we will endeavour to address it as soon as possible. Thank you!

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under an MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>




## Getting Started <a id="gettingstarted"></a>

Slides for the course can be found in the `Slides` directory. The notebooks that cover the content listed below are in the `notebooks` directory.

### Colab <a id="colab"></a>
Download the code from GitHub. Unzip the file and upload it to your Google Drive. In the beginning of the notebooks, there is an optional cell to run which will mount your drive and put you in the correct directory.

### Local <a id="local"></a>
Alternatively, if you're running locally, then just run
```python
pip install -r requirements.txt
```

<p align="right">(<a href="#top">back to top</a>)</p>

## Setting up API Keys <a id="intro-to-APIs"></a>
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

<p align="right">(<a href="#top">back to top</a>)</p>

## Training and Augmenting GPT-2 <a id="finetuning-gpt2"></a>
A walkthrough of using and finetuning a Hugging Face model (GPT-2) can be found in the notebook `finetuning.ipynb`.

This notebook also contains code detailing the construction of a very simple RAG system.

<p align="right">(<a href="#top">back to top</a>)</p>

## Finetuning for classification <a id="bert"></a>
The notebook `BERT_classification.ipynb` contains some code for finetuning smaller models for classification or regression tasks using a simple dataset. It can be modified relatively easily to include your own data.

<p align="right">(<a href="#top">back to top</a>)</p>

## No-code <a id="no-code"></a>
In the workshop, we covered some no-code options:
- [LMStudio](https://lmstudio.ai/)
- [GPT4All](https://gpt4all.io/index.html)
- [Textgen-webui](https://github.com/oobabooga/text-generation-webui)

The easiest to get up and running is LMStudio. If you have a Macbook, it should be very easy to install. You experience with Windows may vary.

GPT4All is also relatively easy to install and get up and running.

Textgen-webui is capable of both inference and some fine-tuning. To get Textgen-webui up and running on your local machine is not too challenging. It is possible to run high-parameter models on the HPC or another remote cluster, and have access to the UI on your local machine. This can be more challenging, so if you're interested in doing this, and get stuck, get in touch with us.

<p align="right">(<a href="#top">back to top</a>)</p>

## Stable Diffusion <a id="stable-diffusion"></a>
You can find a very brief introduction to producing images with Stable Diffusion in the notebook titled `introduction_to_stable_diffusion.ipynb`. This should run on a Macbook or Colab.

In addition to the above no-code options, there is also [ComfyUI](https://github.com/comfyanonymous/ComfyUI), a UI for running Stable Diffusion model checkpoints and LoRAs. This will be slow when running on a laptop, but as with Textgen-webui, ComfyUI can also be run on a remote GPU. There are numerous tutorials online and on YouTube for ComfyUI ([here](https://stable-diffusion-art.com/comfyui/) for example).
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/acceleratescience/packaging-publishing.svg?style=for-the-badge
[contributors-url]: https://github.com/acceleratescience/packaging-publishing/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/acceleratescience/packaging-publishing.svg?style=for-the-badge
[forks-url]: https://github.com/acceleratescience/packaging-publishing/network/members
[stars-shield]: https://img.shields.io/github/stars/acceleratescience/packaging-publishing.svg?style=for-the-badge
[stars-url]: https://github.com/acceleratescience/packaging-publishing/stargazers
[issues-shield]: https://img.shields.io/github/issues/acceleratescience/packaging-publishing.svg?style=for-the-badge
[issues-url]: https://github.com/acceleratescience/packaging-publishing/issues
[license-shield]: https://img.shields.io/github/license/acceleratescience/packaging-publishing.svg?style=for-the-badge
[license-url]: https://github.com/acceleratescience/packaging-publishing/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/company/accelerate-programme-for-scientific-discovery/
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
