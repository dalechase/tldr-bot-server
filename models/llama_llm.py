from groq import Groq
from config import GROQ_API_KEY, LLAMA_LLM_MODEL
from .llm_interface import LLMInterface


class LlamaLLM(LLMInterface):

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    
    def query(self, conversation_history):
        """
        Queries the chat model with the given conversation history and returns the generated response.

        Args:
            conversation_history (list): List of messages representing the conversation history.

        Returns:
            str: The generated response from the chat model.
        """

        conversation_history = self.remove_type_keys(conversation_history)

        chat_completion = self.client.chat.completions.create(
            messages=conversation_history,
            model=LLAMA_LLM_MODEL,
        )
                
        return chat_completion.choices[0].message.content


    def remove_type_keys(self, conversation_history):
        """
        Transforms the conversation history by modifying the structure of each message.

        Args:
            conversation_history (list): A list of dictionaries representing the conversation history.

        Returns:
            list: The updated conversation history with the 'type' key removed from each message.
        """

        for message in conversation_history:
            if 'type' in message:
                del message['type']
        return conversation_history
