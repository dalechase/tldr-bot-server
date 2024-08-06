# TL;DR Bot Server
Backend server for demo LLM app

This app allows users to upload a PDF or Text file and ask an AI questions about the document's contents.


Things that can be improved:

1. The conversation history is reformated to account for the differences between OpenAI & Llama at each interaction. This should happen once each time the LLM provider is changed.
2. Add User loggin to allow for controlled access to documents. The contents of uploaded documents would only be available to specific Users or Departments.
3. PDFs and TXT files should be uploaded directly to cloudstorage, then be processed for vector db ingestion.
4. Add an Admin page for VectorDB file management; listing, deletion.


## Install dependecies
`pip install -r requirements.txt`

## Configure flask app
`export FLASK_APP=wsgi`

In the project root folder:

#### Add the following to your ENV:
export OPENAI_API_KEY = <OPENAI_API_KEY>

export PINECONE_API_KEY = <PINECONE_API_KEY>

#### Create the Uploads folder
`cd tldr-bot-server`

`mkdir uploads`

## Run the server
`flask run -h 127.0.0.1 -p 8000`


## Optional:

Add additional llm API keys to the ENV.

To add Llama via Groq:

export GROQ_API_KEY = <GROQ_API_KEY>


### Optional: specify alternate llm in config.py

export LLM_PROVIDER = 'openai' # Can also be 'llama'
