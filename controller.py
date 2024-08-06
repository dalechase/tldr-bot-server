from flask import abort
from typing import Dict, Tuple, IO
from pathlib import Path
from services.vectordb_service import save_file, split_text, add_to_vectordb, vectordb_query
from services.ai_service import query_ai
from config import ALLOWED_EXTENSIONS
from config import USERNAME, DEPARTMENT, LLM_PROVIDER


class Controller:

    def process_file(self, files: Dict[str, Tuple[str, IO, str]]) -> dict:
        """
        Process the uploaded file and perform necessary operations.

        Args:
            files (Dict[str, Tuple[str, IO, str]]): A dictionary containing the uploaded file.

        Returns:
            dict: A dictionary containing the result of the file processing.

        Raises:
            HTTPException: If the 'file' key is not present in the files dictionary.
            HTTPException: If the file extension is not allowed.
        """

        if 'file' not in files:
            abort(400)

        file = files['file']
        
        if file.filename and Path(file.filename).suffix in ALLOWED_EXTENSIONS:
            filename = save_file(file)
            embeddings = split_text(filename, USERNAME, DEPARTMENT)
            add_to_vectordb(embeddings)

            return {'message': 'File uploaded successfully', 'filename': filename}

        abort(400)


    def query(self, history: list) -> dict:
        """
        Query the AI model based on the user's input and the context from Vectordb.

        Args:
            history (list): A list of dictionaries containing the conversation history.

        Returns:
            dict: A dictionary containing the response from the AI model.
        """

        system_prompt = """System Prompt: Be a chatbot system that depends solely on information from uploaded PDF and text files. 
                           Prioritize data retrieval based on Vectordb Context. If Vectordb Context does not provide relevant information, 
                           respond with a message indicating you don't have the requested data and suggest uploading a relevant document."""

        user_query = history[-1]['content']
        vectordb_result = vectordb_query(user_query, USERNAME, DEPARTMENT)

        text_input = f"System Prompt: {system_prompt}\n\n Vectordb Context: {vectordb_result}\n\n User query: {user_query}"
        history[-1]['content'] = text_input

        ai_response = query_ai(history, llm_name=LLM_PROVIDER)
        

        return {'message': 'Query received', 'text': ai_response}

