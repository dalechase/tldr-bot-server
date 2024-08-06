from models.openai_llm import OpenAILLM
from models.llama_llm import LlamaLLM


def get_llm(llm_name: str) -> object:
    """
    Returns an instance of the specified LLM (Language Model Manager) based on the given llm_name.

    Args:
        llm_name (str): The name of the LLM to retrieve.

    Returns:
        LLM: An instance of the specified LLM.

    Raises:
        ValueError: If the llm_name is not supported.

    """

    if llm_name == "openai":
        return OpenAILLM()
    elif llm_name == "llama":
        return LlamaLLM()
    else:
        raise ValueError(f"Unsupported LLM: {llm_name}")
