# Basic RAG with streamlit for Q&A on .pdf files
Set up a virtual environment, then install the requirements:
```bash
pip install -r requirments.txt
```

# Example usage
In the terminal, run:
```
streamlit run app.py
```

Drag and drop a pdf file from your file explorer (or via the "Browse files" button). This may take a while to load. Use the file named `example.pdf`, included in this package.

You can get summaries:

![summary](https://github.com/rkdan/pdfReader/blob/main/img/summary.png?raw=True)

or ask specific questions:

![specific](https://github.com/rkdan/pdfReader/blob/main/img/specific.png?raw=True)
