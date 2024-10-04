# Introduction to Streamlit
Building nice looking front-end systems is _**hard**_. And it's not something that we really want to spend a lot of time doing. Fortunately, some very smart people have spent a lot of time and effort to make this process easier for us, and developed some frameworks.

Streamlit is a fast and lightweight framework to develop proof of concept applications without having to deep dive into libraries like Django or Flask.

Streamlit is usually run from the command line using

```bash
streamlit run my_app.py [-- any arguments]
```

or

```bash
python -m streamlit run my_app.py
```

This means that we can't run things in a jupyter notebook, and will have to use `.py` files. But that's OK, because that's really where we should be doing most of our developing anyway.

Streamlit has an extensive documentation library that can help you develop specific applications. During this section, we will set out with a goal in mind, and just address things as they come up. Our goal for this section is to develop an application that when we input some topic sentence, an abstract is given to us, along with an AI generated image that describes the abstract!

## First steps
In the first go, we will just focus on showing the abstract on the screen.

### Getting started

First, we need to create a new folder in our root directory called `abstract-application`. We then add a new file called `app.py`.

We have a bunch of code that we can reuse from the prompting exercise we did earlier. We can also copy over the prompt templates. So copy over the `system.jinja` and `user.jinja` files from the `prompt` folder we used in the **Prompting** section.

From here on, you can follow along in order, adding the code to you application.

### Imports
We need the following imports:

```python linenums="1"
import streamlit as st
from openai import OpenAI
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
from typing import Any
import os
import dotenv
```

and we also need to load the environment variables

```python linenums="9"
dotenv.load_dotenv()
```

### Functions from the **Prompting** section
We can just copy over the previous functions:

```python title="Generate the chat response" linenums="11"
def chat_response(system_prompt : str, user_prompt : str, model : str, temperature : float) -> str:
    client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
        max_tokens=400
    ).choices[0].message.content

    return response
```

```python title="Generate the abstract" linenums="27"
def generate_abstract(topic : str) -> str:
    generation_system_prompt = load_template("./prompts/system.jinja", {})
    generation_user_prompt = load_template(
        "./prompts/user.jinja",
        {
            "topic": topic,
        }
    )

    fake_abstract = chat_response(generation_system_prompt, generation_user_prompt, "gpt-4o-mini", 0.2)

    return fake_abstract
```

### Template Loading
We also use the same template loading function, but with some minor changes. Firstly, it's good to just add some error handling, and also we need to tell Jinja where to look. This will be required for running the application in Codespaces.

```python title="Get the template" linenums="41"
def load_template(template_filepath: str, arguments: dict[str, Any]) -> str:
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__)) # (1)!
        # Set up the Jinja environment with the correct base path
        env = Environment(
            loader=FileSystemLoader(searchpath=current_dir),
            autoescape=select_autoescape()
        )
        template = env.get_template(template_filepath)
        return template.render(**arguments)

    except TemplateNotFound:
        st.error(f"Template file not found: {template_filepath}")
        return None
```

1.  This is the only difference. We essentially have to find the absolute path of the current directory that the application is running in, so we can then find the path of the jinja template _relative_ to that path.

### The Streamlit components
Now we start actually adding the streamlit parts, and it's actually really simple. Streamlit has a number of predefined building blocks for us to use, also called _widgets_.

The first two are the `title` and `text_input` widgets.

```python title="Title and input" linenums="58"
# Streamlit app
st.title("Fake Abstract Generator")

# User input
topic = st.text_input("Enter a topic sentence:")
```
The title and a text input field will appear at the top of the page. The `text_input` widget will be a single line, but if you want a commonly used "short answer" style text box, then you can use `text_area`. They do the same thing; the only difference is aesthetics.

The next widget is a `button`. In Streamlit, whenever something is interacted with on the screen, your script is run again. This is essentially what we want - everytime someone presses the button, we want to grab the input text and generate the abstract.

```python title="Button" linenums="64"
# Generate button
if st.button("Generate Abstract"):
    if topic:
        with st.spinner("Generating abstract..."):
            abstract = generate_abstract(topic)
        st.subheader("Generated Abstract:")
        st.write(abstract)
    else:
        st.warning("Please enter a topic sentence.")
```

What you can nest inside the button:
- Transient messages that immediately disappear.
- Once-per-click processes that saves data to session state, a file, or a database.

What you should not nest inside a button:
- Displayed items that should persist as the user continues.
- Other widgets which cause the script to rerun when used.
- Processes that neither modify session state nor write to a file/database, expect when producing disposable results (which we essentially are).

#### Session States
If we want to maintain the button state while we are interacting with other things, we have to use something called `session_state`. This will persist states across runs. We will use this later...but not now...

If what you want is like a toggle switch, then there is a `checkbox`.

Finally, we add a `sidebar`. These things are pretty important, and can be used to manage multipage applications, and store information about your session. They are also commonly where you can put controls like sliders and checkboxes.

```python title="Extra decoration" linenums="74"
# Add some information about the app
st.sidebar.header("About")
st.sidebar.info(
    "This app generates fake abstracts based on a given topic sentence using AI. "
    "Enter a topic and click 'Generate Abstract' to see the result."
)
```

## Adding an image