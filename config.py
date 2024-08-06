import os


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_CLOUD = 'aws'
PINECONE_REGION = 'us-east-1'

LLM_PROVIDER = 'openai'
DEFAULT_LLM_PROVIDER = 'openai'
OPENAI_LLM_MODEL = 'gpt-4o-mini'
LLAMA_LLM_MODEL = 'llama3-8b-8192'

ALLOWED_EXTENSIONS = ['.pdf', '.txt']

INDEX_NAME = 'documents-0000-0000-0000-0001'
USERNAME = 'fauntleroy'
DEPARTMENT = 'visual-effects'
