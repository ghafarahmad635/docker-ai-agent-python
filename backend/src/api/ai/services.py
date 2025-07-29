from api.ai.llm_base import get_openai_llm
from api.ai.schema import EmailMessageSchema
def generate_email_message(query:str) -> EmailMessageSchema:
    llm_base = get_openai_llm()
    llm = llm_base.with_structured_output(EmailMessageSchema)
    messages = [
        (
            "system",
            "You are a helpful assistant for research and composing plaintext emails. Do not use markdown in your response only plaintext.",
        ),
        ("human", f"{query}. Do not use markdown in your response only plaintext"),
    ]
    response = llm.invoke(messages)
    return response