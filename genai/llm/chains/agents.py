from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from .retriever import retriever_from_ai_search

from ..prompts import (
    CONTEXTUALIZER_PROMPT,
    ANSWER_PROMPT,
)

def contextualizer_chain():
    llm = ChatOpenAI(temperature = 0, model_name="gpt-4o-mini")
    chain = CONTEXTUALIZER_PROMPT | llm | StrOutputParser()

    return chain

def answer_chain():
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    chain = (
        (lambda variables: {
            **variables,
            "context": retriever_from_ai_search(variables.get("question"))
        })
        | ANSWER_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain