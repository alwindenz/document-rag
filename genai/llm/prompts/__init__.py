from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import os

def load_prompt_template(filename):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, filename)
    
    with open(file_path, "r") as file:
        content = file.read()
    return content

CONTEXTUALIZER_PROMPT = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(load_prompt_template("context.txt")),
    HumanMessagePromptTemplate.from_template("####Question: {question}####")
])

ANSWER_PROMPT = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(load_prompt_template("answer.txt")),
    HumanMessagePromptTemplate.from_template("####Question: {question}####")
])