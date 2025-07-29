import os
from langchain_openai import ChatOpenAI

def get_openai_llm():
    # 1. grab your API key (must be set)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise NotImplementedError(
            "OPENAI_API_KEY is not set in the environment variables"
        )

    # 2. grab your model name or use a default
    #    here we default to the popular gpt-3.5-turbo if nothing is provided
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4.1")

    # 3. build the arguments dict
    llm_args = {
        "api_key":    api_key,
        "model_name": model_name,
    }

    # 4. if you’ve set a base url (e.g. localhost in dev), include it
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        llm_args["base_url"] = base_url

    # 5. construct and return your client
    return ChatOpenAI(**llm_args)
