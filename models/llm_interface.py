from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    def query(self, conversation_history):
        pass
