from .ops.invoke import chain_invoke

from .chains.agents import (
    contextualizer_chain,
    answer_chain
)
from .ops.logging import logger
import json

def initialize_chains():
    chains = {
        "Contextualizer": contextualizer_chain(),
        "Answer": answer_chain()
    }
    return chains

def get_response(question, chat_history):
    chains = initialize_chains()
    input = {"question": question, "chat_history": chat_history}

    logger.info("Entering Contextualizer Chain")
    context_question = chain_invoke(chains["Contextualizer"], input)
    input = {"question": context_question, "chat_history": chat_history}
    logger.info(f"{input}")

    logger.info("Entering Answer Chain")
    answer = chain_invoke(chains["Answer"], input)

    return answer