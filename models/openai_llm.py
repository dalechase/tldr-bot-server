from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_LLM_MODEL
from .llm_interface import LLMInterface


class OpenAILLM(LLMInterface):

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def query(self, conversation_history):
        """
        Sends a query to the OpenAI language model and returns the generated completion.

        Args:
            conversation_history (list): A list of messages representing the conversation history.

        Returns:
            str: The generated completion from the OpenAI language model.
        """

        completion = self.client.chat.completions.create(
            model=OPENAI_LLM_MODEL,
            messages=conversation_history,
            temperature=1.0,
            presence_penalty=0,
            frequency_penalty=0,
            top_p=1,
            stream=False
        )
        
        return completion.choices[0].message.content
